from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import SuspiciousOperation
from django.core.urlresolvers import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import FormView

from site_app.views import OrderedFilteredListViewMixin
from .forms import MessageForm, MessageChatForm
from .models import Dialog, Message


class DialogView(LoginRequiredMixin, DetailView):
    model = Dialog
    form_class = MessageChatForm

    def get_context_data(self, **kwargs):
        context = super(DialogView, self).get_context_data(**kwargs)
        context['form'] = self.form_class()
        return context

    def post(self, request, *args, **kwargs):
        try:
            self.object = self.model.objects.get(pk=int(kwargs['pk']))
        except Dialog.DoesNotExist as e:
            raise SuspiciousOperation('No dialog with such id (id:%s)' % str(kwargs['pk']))
        # print('object = %s' % str(self.object))
        form = self.form_class(request.POST)
        if form.is_valid():
            sender = request.user
            if request.user not in self.object.participants.all() and request.user.pk != self.object.creator.pk:
                raise SuspiciousOperation('Sender %s not in participants of dialog %s' % (str(sender), str(self.object)))
            Message.objects.create(sender=sender, dialog=self.object, text=form.cleaned_data['text'])
            return HttpResponseRedirect(reverse_lazy('messaging:dialog', kwargs={'pk': self.kwargs['pk']}))
        context = self.get_context_data(object=self.object, form=form)
        return self.render_to_response(context)  # render(request, self.template_name, {'form': form})


class DialogCreate(LoginRequiredMixin, CreateView):
    model = Dialog
    fields = ['name', 'participants']


class MessageCreateView(LoginRequiredMixin, FormView):
    form_class = MessageForm
    template_name = 'messaging/message_form.html'

    def get_success_url(self):
        return reverse_lazy('messaging:dialog', kwargs={'pk': self.dialog_id})

    def form_valid(self, form, **kwargs):
        if form.cleaned_data['create_new_dialog'] == 'True':
            dialog = Dialog.objects.create(
                creator=self.request.user,
                name=form.cleaned_data['dialog_name']
            )
            participants = [participant['id'] for participant in form.cleaned_data['receivers'].values('id')]
            participants += [self.request.user.id]
            if participants:
                dialog.participants.add(*participants)
        else:
            dialog = form.cleaned_data['dialog']
        Message.objects.create(sender=self.request.user, dialog=dialog, text=form.cleaned_data['text'])
        self.dialog_id = dialog.id
        return super(MessageCreateView, self).form_valid(form)


class DialogListView(LoginRequiredMixin, OrderedFilteredListViewMixin, ListView):
    model = Dialog
    paginate_by = 10

    def get_queryset(self):
        return Dialog.objects.personal(self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DialogListView, self).get_context_data(**kwargs)
        return context
