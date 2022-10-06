odoo.define('gif_larger_amounts.gif_hide_button.js', function (require) {

    const FormController = require('web.FormController');
    const ListController = require('web.ListController');
    const KanbanController = require('web.KanbanController');

    const linea = document.getElementsByClassName('o_field_x2many_list_row_add')

    FormController.include({

            hideLine: function () {
                console.log('Decide This', this.modelName)
                console.log('Decide This', this)
                let data = this.initialState.data.state
                console.log('Estado de la compra: ',data)
                
                // if (this.modelName === "stock.picking") 
                if (this.initialState.viewType === 'form'){ 
                    if (data === 'assigned' || data === 'done' ){
                        console.log('Entro A La Condicional')
                        
                        console.log(linea)
                        // linea.style.visibility = "hidden";
                    
                        for( i in linea.length){
                            linea[i].style.visibility = "hidden"; 
                            // linea[i].style.display = "none"; 
                            console.log("oculto")
                        }
                    }    
                }
            },
            renderButtons: function () {
                this._super.apply(this, arguments);
                this.hideLine();
            },
            reload: function () {
                var self = this;
                return this._super.apply(this, arguments).then(function (res) {
                    self.hideLine();
                    return res;
                });
            },
            saveRecord: function () {
                var self = this;
                return this._super.apply(this, arguments).then(function (res) {
                    self.hideLine();
                    return res;
                })
            }
        });
    })


