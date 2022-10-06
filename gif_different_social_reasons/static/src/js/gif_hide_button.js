odoo.define('gif_different_social_reasons.gif_hide_button.js', function (require) {

    const FormController = require('web.FormController');

    FormController.include({

        updateButtons: function(){
            this._super.apply(this, arguments);
            console.log('This: ')
            console.log(this)
            if(this.initialState.viewType == 'form'){
                $('.o-kanban-button-new').hide()
            }    
        },
    });
});