require("jquery");
require("jquery.serializeObject");
require("jquery.iframe-transport");
require("bootstrap");
require("select2");
var csrf_token = require("node-django-csrf-support")();
var when = require("when/when");
var _ = require("underscore");
var Backbone = require("backbone");
Backbone.$ = $;

var errors = require("errors");
var utils = require("utils");
var mapErrors = utils.mapErrors;
var throwNetError = utils.throwNetError;
var handleErrors = utils.handleErrors;
var formProto = require("formProto");
var modals = require('modals');

function modifyUser(data) {
    var request = $.post("/backend/user/" + data.pk, data, 'json');
    return when(request).then(mapErrors, throwNetError);
}

function deleteUser(id) {
    var request = $.post("/backend/user/delete", {
        id: id
    }, 'json');
    return when(request).then(mapErrors, throwNetError);
}

function requireName() {
    var request = $.post("/backend/user/requireName", 'json');
    return when(request).then(mapErrors, throwNetError);
}

var selectName = [];
requireName().then(_.bind(function(data) {
    selectName = data.selectName;
}, this));

var proto = _.extend({}, formProto);
var UserForm = Backbone.View.extend(_.extend(proto, {
    initialize: function() {
        this.setElement($.parseHTML(UserForm.tpl().trim())[0]);
        this.$alert = this.$("p.alert");
        this.$(".glyphicon-info-sign").tooltip();
    },


    setUser: function(user) {
        _.each(['name'], _.bind(function(attr) {
            this.el[attr].value = user[attr];
        }, this));
    },

    bind: function(data) {
        var defaults = {
            id: '',
            title: '',
            description: '',
            url: ''
        };
        data = _.defaults(data, defaults);
        _.each(['name'], _.bind(function(attr) {
            this.el[attr].value = data[attr];
        }, this));
    },

    initName: function() {
        this.$("[name=name]").select2({
            data: selectName,
            formatNoMatches: '没有相关信息',
        });
    },

    onShow: function() {
        this.initName();
    },

    clear: function() {
        _.each(['name'], _.bind(function(field) {
            $(this.el[field]).val('');
        }, this));
        this.clearTip();
    },

    onHide: function() {
        this.clear();
        this.clearErrors(['name'])
    },

    getData: function() {
        var data = {
            'pk': parseInt(this.el.name.value)
        }

        return data;
    },

    validate: function() {
        this.clearErrors(['name']);
        this.clearTip();

        if(this.el.name.value === ""){
            this.addError(this.el.name, '这是必填项！');
            return false;
        }
        return true;
    },

    save: function() {
        var onComplete = _.bind(function() {
            this.trigger('save');
        }, this);

        if (!this.validate()) {
            return setTimeout(onComplete, 0);
        }

        var onReject = _.bind(function(err) {
            handleErrors(err,
                _.bind(this.onAuthFailure, this),
                _.bind(this.onCommonErrors, this),
                _.bind(this.onUnknownError, this)
            );
        }, this);

        var onFinish = _.bind(function() {
            this.tip('成功！', 'success');
            utils.reload(500);
        }, this);

        var data = this.getData();

        modifyUser(data)
            .then(onFinish, onReject)
            .ensure(onComplete);
    }
}));

$(function() {
    UserForm.tpl = _.template($("#form-tpl").html());

    var form = new UserForm();
    var modal = new modals.FormModal();
    modal.setForm(form);
    $(modal.el).appendTo(document.body);

    $create = $("#add-user");
    $create.click(function() {
        modal.show();
        modal.setTitle('添加工作人员');
        modal.setSaveText("添加", "添加中...");
    });
});

$(function() {
    var modal = new modals.ActionModal();
    modal.setAction(function(id) {
        return deleteUser(id).then(function() {
            utils.reload(500);
        }, function(err) {
            if (err instanceof errors.AuthFailure) {
                window.location = "/backend/login";
            }

            throw err;
        });
    });
    modal.setTitle('删除员工');
    modal.tip('确定要删除吗？');
    modal.setSaveText('删除', '删除中...');
    modal.on('succeed', function() {
        utils.reload(500);
    });
    $("table").on("click", ".delete", function() {
        modal.setId($(this).parent().data('pk'));
        modal.show();
    });
});
