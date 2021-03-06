$(function () {
    $.widget('photoGallery.mainForm', {
        options: {
            // input file field
            fileInput: undefined,
            // Define a list of dictionaries having the id of the fileUI widget, fileUI widget and file object
            filesUI: {},
            // fileUi container
            fileUIContainer: undefined,
            // filter the new add files against already added files,
            xhrOptions: undefined,

            jqXHR: undefined,

            processItems: undefined,

            filter: function (files) {
                let that = this;
                if (that.files === undefined) {
                    return files;
                } else {
                    let newFiles = [];
                    $.each(files, function (index, file) {
                        let isNewFile = true;
                        for (let i = 0; i < that.files.length; i++) {
                            if (that.files[i].name === file.name) {
                                isNewFile = false;
                            }
                        }
                        if (isNewFile) {
                            newFiles.push(file);
                        }
                    });
                    return newFiles;
                }
            }
        },
        _create: function (e) {
            let options = this.options;
            if (options.fileInput === undefined) {
                options.fileInput = this.element.find('input[type=file]');
                options.fileUIContainer = this.element.find('.file-list-container');
                this._on(this.options.fileInput, {
                    change: this._onChange
                });
                this._on(this.element.find('#submitButton'), {
                    click: function (e) {
                        e.preventDefault();
                        this._submit();
                    }
                });
                this._on(this.element.find('#deleteButton'), {
                    'click': function (e) {
                        e.preventDefault();
                        this._deleteAll()
                    }
                });
            }
        },

        /**
         * Bind to input change event
         */
        _onChange: function (event) {
            let that = this,
                options = this.options,
                data = {
                    fileInput: $(event.target)
                };
            let newFiles = $.makeArray(data.fileInput.prop('files'));
            if (newFiles.length > 0) {
                $.when(options.filter(newFiles)).then(function (newFiles) {
                        $.map(newFiles, function (file) {
                            let element = that._createUI(file);
                            that.options.filesUI[element.fileui('option', 'id')] = element;
                        });
                    }
                );
            }
            $(event.target).val("");
        },

        /**
         * Return the newly created element for file
         */
        _createUI: function (file) {
            let that = this,
                options = this.options;
            let newElement = $("<div></div>").fileui({
                'filename': file.name,
                'file': file
            });
            that._on(newElement.fileui(), {
                'fileuidelete': that._deleteUI
            });
            newElement.appendTo(options.fileUIContainer);
            return newElement;
        },

        // Delete UI
        _deleteUI: function (event, data) {
            let options = this.options;
            $.each(options.filesUI, function (id, entry) {
                if (id === data.id) {
                    entry.fileui('abort');
                    entry.fileui('destroy');
                    delete options.filesUI[id];
                    return false;
                }
            });
        },

        _initOptions: function (options) {
            if (!options) {
                options = {}
            }
            options.headers = {};
            options.type = {};
            options.data = {};
            options.url = "";
        },
        // create the ajax settings for signing the files
        _initDataforSigning: function (options) {
            this._initOptions(options);
            options.headers['Content-Type'] = 'application/json';
            options.type = 'POST';
            options.url = '/album/sign-s3/' + this._get_album_id();
            options.headers['X-CSRFToken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            tempData = {};
            $.each(options.filesUI, (idx, value) => {
                tempData[value.fileui('option', 'id')] = {
                    'filename': value.fileui('option', 'filename'),
                    'filetype': value.fileui('option', 'file').type
                };
            });
            options.data = JSON.stringify(tempData)
        },
        _submit: function () {
            let self = this,
                o = this.options;
                uploadResult = {
                    'done': [],
                    'failed': []
                };

            o.processItems = [];

            self._initDataforSigning(o);
            this.jqXHR = $.ajax(o);
            this.jqXHR.done(function (result, textStatus, jqXHR) {
                self._initDataForAws(result);
                $.each(self.options.filesUI, (id, obj) => {
                    const promise = obj.fileui('send');
                    o.processItems.push(promise)
                });

                $.when.apply($, $.map(o.processItems, function(item) {
                    let dfd = $.Deferred();
                    item.done(function(filename) {
                        uploadResult['done'].push(filename);
                    }).fail(function(filename) {
                        uploadResult['failed'].push(filename);
                    }).always(function() {
                        dfd.resolve();
                    });
                    return dfd.promise();
                })).then(function() {
                    self._onFinishedUpload(uploadResult);

                });
            });


        },
        _abort: function () {
            if (this.jqXHR) {
                return this.jqXHR.abort();
            }
        },
        _onFinishedUpload(uploadResults) {
            let self = this;

            let options = {
                'headers': {},
                'type': '',
                'url': '',
                'data': ''
            };
            options.headers['Content-Type'] = 'application/json';
            options.type = 'POST';
            options.url = '/album/upload/' + self._get_album_id();
            options.headers['X-CSRFToken'] = document.getElementsByName('csrfmiddlewaretoken')[0].value;
            options.data = JSON.stringify(uploadResults);

            this.jqXHR = $.ajax(options);
            this.jqXHR.always(function (result, textStatus, jqXHR) {
                console.log(result);
            });
        },
        _deleteAll: function () {
            let options = this.options;
            $.each(options.filesUI, function (id, entry) {
                entry.fileui('destroy');
                delete options.filesUI[id];
            });
            this.options.files = undefined;
        },
        _initDataForAws: function (signed_urls) {
            let o = this.options;
            for (let key in signed_urls) {
                if (key in o.filesUI) {
                    let item = o.filesUI[key];
                    item.fileui('setSignedUrl', signed_urls[key]);
                }
            }
        },
        _get_album_id: function () {
            let href = window.location.href;
            let parts = href.split('/')
            return parts[parts.length - 1]
        }

    });
});