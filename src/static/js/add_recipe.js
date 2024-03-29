var __hasProp = {}.hasOwnProperty,
  __extends = function(child, parent) { for (var key in parent) { if (__hasProp.call(parent, key)) child[key] = parent[key]; } function ctor() { this.constructor = child; } ctor.prototype = parent.prototype; child.prototype = new ctor(); child.__super__ = parent.prototype; return child; };

(function($) {
  var FormsetError;
  $.fn.djangoFormset = function(options) {
    return new $.fn.djangoFormset.Formset(this, options);
  };
  FormsetError = (function(_super) {
    __extends(FormsetError, _super);

    function FormsetError() {
      return FormsetError.__super__.constructor.apply(this, arguments);
    }

    return FormsetError;

  })(Error);
  $.fn.djangoFormset.Formset = (function() {
    function Formset(base, options) {
      var deletedForms, forms, inputName, placeholderPos;
      this.opts = $.extend({}, $.fn.djangoFormset.defaultOptions, options);
      if (base.length === 0) {
        throw new FormsetError("Empty selector.");
      }
      this.template = base.filter("." + this.opts.formTemplateClass);
      if (this.template.length === 0) {
        throw new FormsetError("Can't find template (looking for ." + this.opts.formTemplateClass + ")");
      }
      inputName = this.template.find("input,select,textarea").first().attr('name');
      if (!inputName) {
        throw new FormsetError("Can't figure out form prefix because there's no form element in the form template. Please add one.");
      }
      placeholderPos = inputName.indexOf('-__prefix__');
      if (placeholderPos === -1) {
        throw new FormsetError("Can't figure out form prefix from template because it doesn't contain '-__prefix__'.");
      }
      this.prefix = inputName.substring(0, placeholderPos);
      this.totalForms = $("#id_" + this.prefix + "-TOTAL_FORMS");
      if (this.totalForms.length === 0) {
        throw new FormsetError("Management form field 'TOTAL_FORMS' not found for prefix " + this.prefix + ".");
      }
      this._initTabs();
      forms = base.not("." + this.opts.formTemplateClass);
      this.initialForms = forms.length;
      $(this).on(this.opts.on);
      this.forms = forms.map((function(_this) {
        return function(index, element) {
          var newForm, tab, tabActivator;
          if (_this.hasTabs) {
            tabActivator = $.djangoFormset.getTabActivator(element.id);
            tab = new _this.opts.tabClass(tabActivator.closest('.nav > *'));
          }
          newForm = new _this.opts.formClass($(element), _this, index, tab);
          $(_this).trigger("formInitialized", [newForm]);
          return newForm;
        };
      })(this));
      if (this.forms.length !== parseInt(this.totalForms.val())) {
        console.error("TOTAL_FORMS is " + (this.totalForms.val()) + ", but " + this.forms.length + " non-template elements found in passed selection.");
      }
      deletedForms = this.forms.filter(function() {
        return this.deleteInput.val();
      });
      deletedForms.each(function() {
        return this["delete"]();
      });
      this.insertAnchor = base.not("." + this.opts.formTemplateClass).last();
      if (this.insertAnchor.length === 0) {
        this.insertAnchor = this.template;
      }
      return;
    }

    Formset.prototype._initTabs = function() {
      var tabActivator, tabNav;
      this.hasTabs = this.template.is('.tab-pane');
      if (!this.hasTabs) {
        return;
      }
      tabActivator = $.djangoFormset.getTabActivator(this.template.attr('id'));
      if (tabActivator.length === 0) {
        throw new FormsetError("Template is .tab-pane but couldn't find corresponding tab activator.");
      }
      tabNav = tabActivator.closest('.nav');
      if (tabNav.length === 0) {
        throw new FormsetError("Template is .tab-pane but couldn't find corresponding .nav.");
      }
      this.tabTemplate = tabNav.children("." + this.opts.formTemplateClass);
      if (this.tabTemplate.length === 0) {
        throw new FormsetError("Tab nav template not found (looking for ." + this.opts.formTemplateClass + ").");
      }
    };

    Formset.prototype.addForm = function() {
      var newForm, newFormElem, newTab, newTabElem, tabInsertAnchor;
      if (this.hasTabs) {
        newTabElem = this.tabTemplate.clone().removeClass(this.opts.formTemplateClass);
        newTab = new this.opts.tabClass(newTabElem);
        if (this.forms.length > 0) {
          tabInsertAnchor = this.forms[this.forms.length - 1].tab.elem;
        } else {
          tabInsertAnchor = this.tabTemplate;
        }
        newTabElem.insertAfter(tabInsertAnchor);
      }
      newFormElem = this.template.clone().removeClass(this.opts.formTemplateClass);
      newForm = new this.opts.formClass(newFormElem, this, parseInt(this.totalForms.val()), newTab);
      newFormElem.insertAfter(this.insertAnchor);
      this.insertAnchor = newFormElem;
      this.forms.push(newForm);
      this.totalForms.val(parseInt(this.totalForms.val()) + 1);
      if (this.hasTabs) {
        newTab.activate();
      }
      $(this).trigger("formInitialized", [newForm]);
      $(this).trigger("formAdded", [newForm]);
      return newForm;
    };

    Formset.prototype.deleteForm = function(index) {
      var form;
      form = this.forms[index];
      form["delete"]();
    };

    Formset.prototype.handleFormRemoved = function(index) {
      var form, i, _i, _len, _ref;
      this.totalForms.val(parseInt(this.totalForms.val()) - 1);
      this.forms.splice(index, 1);
      _ref = this.forms;
      for (i = _i = 0, _len = _ref.length; _i < _len; i = ++_i) {
        form = _ref[i];
        form._updateFormIndex(i);
      }
      if (this.forms.length === 0) {
        this.insertAnchor = this.template;
      } else {
        this.insertAnchor = this.forms[this.forms.length - 1].elem;
      }
    };

    return Formset;

  })();
  $.fn.djangoFormset.Form = (function() {
    function Form(elem, formset, index, tab) {
      var isInitial;
      this.elem = elem;
      this.formset = formset;
      this.index = index;
      this.tab = tab;
      this.elem.data('djangoFormset.Form', this);
      if (this.index !== void 0) {
        this._initFormIndex(this.index);
      }
      this.deleteInput = this.field('DELETE');
      isInitial = this.index < this.formset.initialForms;
      if (this.deleteInput.length > 0 || !isInitial) {
        this._replaceDeleteCheckboxWithButton();
      }
    }

    Form.prototype.getDeleteButton = function() {
      return $("<div> " + this.formset.opts.deleteButtonText + " </div>");
    };

    Form.prototype.insertDeleteButton = function() {
      if (this.deleteInput.length > 0) {
        this.deleteInput.after(this.deleteButton);
      } else {
        (this.elem.is('TR') ? this.elem.children().last() : this.elem.is('UL') || this.elem.is('OL') ? this.elem.append('li').children().last() : this.elem).append(this.deleteButton);
      }
    };

    Form.prototype["delete"] = function() {
      var isInitial, nextTab, tabElems;
      isInitial = this.index < this.formset.initialForms;
      if (this.deleteInput.length === 0 && isInitial) {
        console.warn("Tried do delete non-deletable form " + this.formset.prefix + " #" + this.index + ".");
        return;
      }
      if (this.tab && this.tab.elem.is('.active')) {
        tabElems = this.formset.forms.map(function(index, form) {
          return form.tab.elem[0];
        });
        nextTab = tabElems.slice(this.index + 1).filter(':visible').first();
        if (nextTab.length === 0) {
          nextTab = tabElems.slice(0, this.index).filter(':visible').last();
        }
        if (nextTab.length > 0) {
          nextTab.data('djangoFormset.tab').activate();
        }
      }
      if (isInitial) {
        if (this.deleteInput.length > 0) {
          this.deleteInput.val('on');
        }
        if (this.tab) {
          this.tab.elem.hide();
        }
        this.hide();
      } else {
        if (this.tab) {
          this.tab.elem.remove();
        }
        this.elem.remove();
        this.formset.handleFormRemoved(this.index);
      }
    };

    Form.prototype.hide = function() {
      return this.elem.hide();
    };

    Form.prototype.field = function(name) {
      return this.elem.find("[name='" + this.formset.prefix + "-" + this.index + "-" + name + "']");
    };

    Form.prototype.prev = function() {
      var form, _i, _ref;
      _ref = this.formset.forms.slice(0, +(this.index - 1) + 1 || 9e9);
      for (_i = _ref.length - 1; _i >= 0; _i += -1) {
        form = _ref[_i];
        if (form.elem.is(':visible')) {
          return form;
        }
      }
    };

    Form.prototype._replaceDeleteCheckboxWithButton = function() {
      var label, newDeleteInput;
      if (this.deleteInput.length > 0) {
        newDeleteInput = $("<input type='hidden' name='" + (this.deleteInput.attr('name')) + "' id='" + (this.deleteInput.attr('id')) + "' value='" + (this.deleteInput.is(':checked') ? 'on' : '') + "'/>");
        label = this.elem.find("label[for='" + (this.deleteInput.attr('id')) + "']");
        if (label.has(this.deleteInput).length > 0) {
          label.replaceWith(newDeleteInput);
        } else {
          label.remove();
          this.deleteInput.replaceWith(newDeleteInput);
        }
        this.deleteInput = newDeleteInput;
      }
      this.deleteButton = this.getDeleteButton();
      this.deleteButton.on('click', (function(_this) {
        return function(event) {
          return _this["delete"]();
        };
      })(this));
      this.insertDeleteButton();
    };

    Form.prototype._replaceFormIndex = function(oldIndexPattern, index) {
      var newPrefix, prefixRegex, _replaceFormIndexElement;
      this.index = index;
      prefixRegex = new RegExp("" + this.formset.prefix + "-" + oldIndexPattern);
      newPrefix = "" + this.formset.prefix + "-" + index;
      _replaceFormIndexElement = function(elem) {
        var attributeName, attributeNames, attributeNamesByTagName, tagName, _i, _len, _results;
        attributeNamesByTagName = {
          input: ['id', 'name'],
          select: ['id', 'name'],
          textarea: ['id', 'name'],
          label: ['for'],
          div: ['id'],
          '*': ['href', 'data-target']
        };
        tagName = elem.get(0).tagName;
        attributeNames = [];
        if (tagName.toLowerCase() in attributeNamesByTagName) {
          attributeNames = attributeNamesByTagName[tagName.toLowerCase()];
        }
        attributeNames.push.apply(attributeNames, attributeNamesByTagName['*']);
        _results = [];
        for (_i = 0, _len = attributeNames.length; _i < _len; _i++) {
          attributeName = attributeNames[_i];
          if (elem.attr(attributeName)) {
            _results.push(elem.attr(attributeName, elem.attr(attributeName).replace(prefixRegex, newPrefix)));
          } else {
            _results.push(void 0);
          }
        }
        return _results;
      };
      _replaceFormIndexElement(this.elem);
      this.elem.find('input, select, textarea, label').each(function() {
        _replaceFormIndexElement($(this));
      });
      if (this.tab) {
        _replaceFormIndexElement(this.tab.elem);
        this.tab.elem.find('a, button').each(function() {
          _replaceFormIndexElement($(this));
        });
      }
    };

    Form.prototype._initFormIndex = function(index) {
      this._replaceFormIndex("__prefix__", index);
    };

    Form.prototype._updateFormIndex = function(index) {
      this._replaceFormIndex('\\d+', index);
    };

    return Form;

  })();
  $.fn.djangoFormset.Tab = (function() {
    function Tab(elem) {
      this.elem = elem;
      this.elem.data('djangoFormset.tab', this);
    }

    Tab.prototype.activate = function() {
      return this.elem.find("[data-toggle='tab']").trigger('click');
    };

    Tab.prototype.remove = function() {
      return this.elem.remove();
    };

    return Tab;

  })();
  $.fn.djangoFormset.defaultOptions = {
    formTemplateClass: 'empty-form',
    formClass: $.fn.djangoFormset.Form,
    tabClass: $.fn.djangoFormset.Tab,
    deleteButtonText: 'Delete'
  };
  $.djangoFormset = {
    getTabActivator: function(id) {
      return $("[href='#" + id + "'], [data-target='#" + id + "']");
    }
  };
})(jQuery);

showSubCategory()
function showSubCategory() {
    //        <!--Dependence dropdown-->
    $('#id_category').change(function (e) {
        e.preventDefault();
        $('#id_sub_category').children().remove()
        $('#id_sub_category').siblings('div .text').html('---------')
        var pk = $('#id_category').val()
        const url = $('.recipe_box_category').attr('data-href-template')
        let csrf = $('input[name=csrfmiddlewaretoken]').val()
        $.ajax({
            type: 'GET',
            url: url,
            data: { 'category_id': pk, 'csrfmiddlewaretoken': csrf },
            dataType: 'json',
            success: function (response) {
                if (response.length > 0) {
                    option = '<option value="" selected="True">---------</option>'
                    response.forEach(function (subcats) {
                        option += `<option value="${subcats.id}">${subcats.name}</option>`
                    })
                    $('#id_sub_category').append(option)
                } else {
                    $('#id_sub_category').children().remove()
                }
            },
            error: function (rs, e) {
                console.log(rs.responseText);
            },
        });
    });
}


$(document).ready(function () {
    //<!--        Semantic ui checkbox and dropdown -->
    $('.max.example ui.normal.dropdown').dropdown({ maxSelections: 3 });
    $('.my_dropdown').dropdown();
    $('.ui.toggle.checkbox').checkbox();

    //<!--on click poster image start image downloader-->
    $('#poster_image_id').click(() => {
        $('#id_poster').click()
    })
    // Hover on image show icons
    $('#poster_image_id').mouseover(() => {
        $('.form__add-img').css({ 'display': 'block' })
    })
    $('#poster_image_id').mouseout(() => {
        $('.form__add-img').css({ 'display': 'none' })
    })
    $('.instruction_image_div').mouseover((e) => {
        $(e.target).next().next('div.form__add-img-instr').css({ 'display': 'block', })
    })
    $('.instruction_image_div').mouseout((e) => {
        $(e.target).next().next('div.form__add-img-instr').css({ 'display': 'none', })
    })

    // Show on temporary window image which was selected
    $('.instruction_image_div').click((e) => {
        var next_elemn_div = $(e.target).next()
        var hiden_inputload_image_instractuin = next_elemn_div.children('input[type=file]')
        hiden_inputload_image_instractuin.click()
        hiden_inputload_image_instractuin.change((e) => {
            if ($(e.target).prop('files') && $(e.target).prop('files')[0]) {
                previousImage = next_elemn_div.prev()
                var reader = new FileReader()
                reader.onload = function (e) {
                    var image = e.target.result
                    previousImage.attr({ 'src': image })
                }
                reader.readAsDataURL($(e.target).prop('files')[0])
            }
        })
    })

})

//<!--Show image on temporary window-->
function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader()
        reader.onload = function (e) {
            var image = e.target.result
            var imageField = document.getElementById('poster_image_id')
            imageField.src = image
        }
        reader.readAsDataURL(input.files[0])
    }
}


var outerFormset = $("fieldset.ingredient_form_set").not('.ui.negative.message')
    .djangoFormset({
        on: {
            formInitialized: function (event, form) {
                /* Init inner formset */
                var innerFormsetElem = form.elem.children('div.ingredient_block');

                var innerFormset = innerFormsetElem.children('div').djangoFormset({
                    deleteButtonText: '<i class="ui big times circle red icon cursor"></i>',
                });

                innerFormsetElem.on('click', '[data-action=add-inner-ingredient-form]', function (event) {
                    innerFormset.addForm();
 
                });

            },
        },
        deleteButtonText: '<i class="ui big times circle red icon cursor"></i>',
    });

/* Add new outer form on add button click */
$('form').on('click', '[data-action=add-outer-ingredient-form]', function (event) {
    outerFormset.addForm();
});
$(function () {
    var formset = $('div.inline.instruction_visible').djangoFormset({
        deleteButtonText: '<i class="ui big times circle red icon cursor"></i>',
    });

    $('form').on('click', '[data-action=add-form-to-instruction]', function (event) {
        formset.addForm();
        // Show on temporary window image which was selected
        $('.instruction_image_div').click((e) => {
            var next_elemn_div = $(e.target).next()
            var hiden_inputload_image_instractuin = next_elemn_div.children('input[type=file]')
            hiden_inputload_image_instractuin.click()

            hiden_inputload_image_instractuin.change((e) => {
                if ($(e.target).prop('files') && $(e.target).prop('files')[0]) {
                    previousImage = next_elemn_div.prev()
                    var reader = new FileReader()
                    reader.onload = function (e) {
                        var image = e.target.result
                        previousImage.attr({ 'src': image })
                    }
                    reader.readAsDataURL($(e.target).prop('files')[0])
                }
            })
        })
        // <!--  Hovering on instruction image          -->
        $('.instruction_image_div').mouseover((e) => {
            $(e.target).next().next('div.form__add-img-instr').css({ 'display': 'block', })
        })
        $('.instruction_image_div').mouseout((e) => {
            $(e.target).next().next('div.form__add-img-instr').css({ 'display': 'none', })
        })
    });
});