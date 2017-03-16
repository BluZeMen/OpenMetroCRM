/**
 * Created by bzm on 04.01.17.
 */

var switchers = {
    /**
     * Helper func for finding elements in html document with behavior
     * @param behavior - name of behavior
     */
    findElemsWithBehavior: function (behavior) {
        var elements = $.map($('[behavior="' + behavior + '"]'), function (sw) {
            return sw.attributes['name'].value;
        });

        // remove duplicates
        var cnt =  elements.length;
        for(var i = 0, ioe; i < cnt; i++){
            for(ioe = cnt - 1; ioe != i; ioe--){
                if(elements[i] == elements[ioe] && ioe != i){
                    elements.splice(ioe, 1);
                }
            }
        }
        return elements;
    },
    /**
     * Helper func enabling element of map
     * @param currentSwitchState - current state of switch
     * @param map - map of switch values to elements
     */
    setVisible: function (currentSwitchState, map) {
        var el;
        for(var elem in map) {
            el = $($('#id_' + elem).parents()[1]);
            if(currentSwitchState == map[elem]){
                el.hide();
                // console.log('hide=', el);
            }else{
                el.show();
                // console.log('show=', el);
            }
        }
    },
    /**
     * Helper to set items enabling by radio switch in form
     * @param switcher - form name of switcher
     * @param map - map of switch value to input value
     */
    addSwitcher: function (switcher, map) {
        var that = this;
        $('input[name=' + switcher + ']').on('change', function () {
            var val = that.getValue(switcher);
            if(val == $(this).val()){
                that.setVisible(val, map);
            }
        });
    },

    initSwitcher: function (switcher, map) {
        var val = this.getValue(switcher);
        this.setVisible(val, map);
    },

    getSwitchingMapOf: function (switchName) {
        return JSON.parse($('[name="'+ switchName +'"]')[0].attributes['switch-items'].value);
    },

    getValue: function (switchName) {
        return $('input[name=' + switchName + ']:checked').val();
    },

    init: function () {
        var switchers = this.findElemsWithBehavior('switch-ui-enabler');
        var val, map;
        for(var sw=switchers[0], i=0; i < switchers.length; sw=switchers[i++]){
            map = this.getSwitchingMapOf(sw);
            this.addSwitcher(sw, map);
            this.initSwitcher(sw, map)
        }
        // console.log('switchers =', switchers);
        // for(var sw in switchers){
        //     console.log('sw =', sw);
        //     this.addSwitcher(sw, this.getSwitchingMapOf(sw));
        // }
    }
};


/**
 * Autorun
 */
$(document).ready(function () {
    switchers.init();
});
