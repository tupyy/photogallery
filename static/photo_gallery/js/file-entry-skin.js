$(function () {
    $.widget("photoGallery.fileUISkin", {

        _create: function () {
            this.element.addClass("upload-file");
            this.mainElement = $("<div></div>", {
                "class": "file-ui"
            }).appendTo(this.element);

            this.label = $("<span></span>", {
                text: this.options.filename,
                "class": "col-xs-2 file-label"
            }).appendTo(this.mainElement);

            this.progressDiv = $("<div></div>", {
                "class": "col progress"
            }).appendTo(this.mainElement);

            this.progressBar = $("<div></div>", {
                "class": "progress-bar bg-success",
                "style": "width: 0%"
            }).appendTo(this.progressDiv);

            this.deleteButton = $("<button>", {
                text: "Delete",
                "class": "ui-upload-button btn btn-danger"
            }).appendTo(this.mainElement)
                .button();

            this._on(this.deleteButton, {
                click: function(e) {
                    e.preventDefault();
                    this._delete();
                }
            });
        },

        refresh: function (progress) {
            this.progressBar.attr('style','width: ' + progress + '%')
        },
    });
});
