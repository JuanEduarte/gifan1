odoo.define('gif_business_flow_segregation.gif_hide_line.js', function (require) {
    const FormController = require('web.FormController');
    const ListView = require('web.ListView');
    const ListRenderer = require('web.ListRenderer');
    const BasicController = require('web.BasicController');;


    BasicController.include({
        _getPagingInfo: function (state) {
            model = this.modelName
            view = this.viewType
            if (model === "sale.order" && view === "list") {
                var counter = 0
                var data_count = this.initialState.data
                for (data in data_count) {
                    if (data_count[data].data.suma === 3) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 1) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 2) {
                        if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 4) {
                        if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 5) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 7) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else { }
                    }
                }
                const isGrouped = state.groupedBy && state.groupedBy.length;
                return {
                    currentMinimum: (isGrouped ? state.groupsOffset : state.offset) + 1,
                    limit: isGrouped ? state.groupsLimit : counter,
                    size: isGrouped ? state.groupsCount : counter,
                };
            } else if (model === "purchase.order" && view === "list") {
                var counter = 0
                var data_count = this.initialState.data
                for (data in data_count) {
                    if (data_count[data].data.suma === 3) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 1) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 2) {
                        if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 4) {
                        if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                       
                    } else if (data_count[data].data.suma === 8) {
                        if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 16) {
                        if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 5) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 6) {
                        if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 9) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 10) {
                        if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 12) {
                        if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 17) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 18) {
                        if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 20) {
                        if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 24) {
                        if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 7) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 11) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 13) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 14) {
                        if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 14) {
                        if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 19) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 21) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 22) {
                        if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 25) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 26) {
                        if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 28) {
                        if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 15) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 23) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 27) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 29) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 30) {
                        if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else { }
                    } else if (data_count[data].data.suma === 31) {
                        if (data_count[data].data.is_primary === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_insume === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_office === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_ben_dis === true) {
                            counter = counter + 1
                        }
                        else if (data_count[data].data.is_associated === true) {
                            counter = counter + 1
                        }
                        else { }
                    }
                }
                const isGrouped = state.groupedBy && state.groupedBy.length;
                return {
                    currentMinimum: (isGrouped ? state.groupsOffset : state.offset) + 1,
                    limit: isGrouped ? state.groupsLimit : counter,
                    size: isGrouped ? state.groupsCount : counter,
                };

            } else {
                const isGrouped = state.groupedBy && state.groupedBy.length;
                return {
                    currentMinimum: (isGrouped ? state.groupsOffset : state.offset) + 1,
                    limit: isGrouped ? state.groupsLimit : state.limit,
                    size: isGrouped ? state.groupsCount : state.count,
                };
            }
        }

    });

    FormController.include({

        getTitle: function () {
            let model = this.initialState.model
            if (model === 'sale.order') {
                $('.fa-chevron-left').hide()
                $('.fa-chevron-right').hide()
            }
            else if (model === 'purchase.order') {
                $('.fa-chevron-left').hide()
                $('.fa-chevron-right').hide()
            }
            return this.model.getName(this.handle);
        },

    });

    ListRenderer.include({

        /**
        * Render a row, corresponding to a record.
        *
        * @private
        * @param {Object} record
        * @returns {jQueryElement} a <tr> element
        */
        _renderRow: function (record) { 
            let data_show = this.state.data
            var self = this;
            var $cells = this.columns.map(function (node, index) {
                return self._renderBodyCell(record, node, index, { mode: 'readonly' });
            });
            let model_show = this.state.model
            for (data in data_show) {
                if (model_show === 'sale.order') {
                    if ($cells[0][0].title === data_show[data].data.name) {
                        if (data_show[data].data.suma == 7) {
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 1) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 2) {
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 4) {
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { }//Comienza otra condición.
                        if (data_show[data].data.suma == 3) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 5) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 6) {
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                    }
                }
                else if (model_show === 'purchase.order') {
                    if ($cells[1][0].title === data_show[data].data.name) {
                        if (data_show[data].data.suma == 7) {
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 1) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 2) {
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 4) {
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { }//Comienza otra condición.
                        if (data_show[data].data.suma == 8) {
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 16) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 3) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 9) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 17) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 5) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 10) {
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 24) {
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 12) {
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 18) {
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 6) {
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 20) {
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condicion
                        if (data_show[data].data.suma == 11) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 25) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 13) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 19) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 21) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 14) {
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 26) {
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 22) {
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 26) {
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 28) {
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 15) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 23) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 27) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 29) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición
                        if (data_show[data].data.suma == 30) {
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { } //Comienza otra condición 
                        if (data_show[data].data.suma == 31) {
                            if (data_show[data].data.is_primary === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_insume === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_ben_dis === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_associated === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                            if (data_show[data].data.is_office === true) {
                                var $tr = $('<tr/>', { class: 'o_data_row' })
                                    .attr('data-id', record.id)
                                    .append($cells);
                                if (this.hasSelectors) {
                                    $tr.prepend(this._renderSelector('td', !record.res_id));
                                }
                                if (this.no_open && this.mode === "readonly") {
                                    $tr.addClass('o_list_no_open');
                                }
                                this._setDecorationClasses($tr, this.rowDecorations, record);
                            } else { }
                        } else { }
                    }
                }
                else {
                    var $tr = $('<tr/>', { class: 'o_data_row' })
                        .attr('data-id', record.id)
                        .append($cells);
                    if (this.hasSelectors) {
                        $tr.prepend(this._renderSelector('td', !record.res_id));
                    }
                    if (this.no_open && this.mode === "readonly") {
                        $tr.addClass('o_list_no_open');
                    }
                    this._setDecorationClasses($tr, this.rowDecorations, record);
                }
            }
            return $tr;
        }
    });

    ListView.include({
        _updateMVCParams: function () {
        }
    });

});
