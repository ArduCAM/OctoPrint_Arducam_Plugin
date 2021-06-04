/*
 * View model for OctoPrint-Arducamfocus
 *
 * Author: Arducam
 * License: AGPLv3
 */
$(function() {
    function ArducamfocusViewModel(parameters) {
        var self = this;
        let til = 90;
        let pan = 90;
        let step = 5;
        self.onBeforeBinding = function() {
            // self.time = self.getTime();
            self.load();
        }
        
        self.load = function() {
            // var row = $('<div class="control-group" <label class="control-label">Arducam Focus Control</label> <div class="controls"><input type="range" class="texto input-block-level" value="512" min="0" max="1023"></div></div>');
            // row.find(".texto").on("input",function() {
            //     var arm= parseInt(this.value);
            //     self.changeServo(arm);                              
            // });
            // $('#control-jog-custom').append(row);
            let tilPan = $('<div id="control-til-pan" class="jog-panel"><h1>ptz-til-pan</h1><div><button id="control-til-up" class="btn box"><i class="fas fa-arrow-up"></i></button></div><div><button id="control-pan-left" class="btn box pull-left"><i class="fas fa-arrow-left"></i></button><button id="contrl-pan-til-label" class="btn box pull-left" style="padding: 0px"></button><button id="control-pan-right" class="btn box pull-left"><i class="fas fa-arrow-right"></i></button></div><div><button id="control-til-down" class="btn box"><i class="fas fa-arrow-down"></i></button></div><div class="btn-group" data-toggle="buttons-radio" id="123"><button id="step1" type="button" class="btn">5</button><button id="step2" type="button" class="btn">10</button><button id="step3" type="button" class="btn">20</button></div></div>')
            tilPan.find("#control-til-up").click(function() {
                til = til + step
                if (til > 180) {
                    til = 180
                }
                $('#contrl-pan-til-label').text(til)
                self.sendReq('ptz_til', til, function() {
                    
                })
            })
            tilPan.find("#control-til-down").click(function() {
                til = til - step
                if (til < 0) {
                    til = 00
                }
                $('#contrl-pan-til-label').text(til)
                self.sendReq('ptz_til', til, function() {
                    
                })
            })
            tilPan.find("#control-pan-left").click(function() {
                pan = pan - step
                if (pan < 0) {
                    pan = 0
                }
                $('#contrl-pan-til-label').text(pan)
                self.sendReq('ptz_pan', pan, function() {
                    
                })
            })
            tilPan.find("#control-pan-right").click(function() {
                pan = pan + step
                if (pan >180) {
                    pan = 180
                }
                $('#contrl-pan-til-label').text(pan)
                self.sendReq('ptz_pan', pan, function() {
                    
                })
            })
            tilPan.find("#step1").click(function() {
                step = 5
            })

            tilPan.find("#step2").click(function() {
                step = 10
            })

            tilPan.find("#step3").click(function() {
                step = 20
            })
            
            $('#control-jog-custom').append(tilPan);

            let focus = $('<div class="jog-panel" style="width: 330px;"><h1>Focus</h1><input id="control-ptz-focus" type="range" class="texto input-block-level" value="10000" min="0" max="20000"><h1>Zoom</h1><input id="control-ptz-zoom" type="range" class="texto input-block-level" value="10000" min="0" max="20000"></div>');
            focus.find("#control-ptz-zoom").on("input",function() {
                const arm= parseInt(this.value);
                self.sendReq('ptz_zoom', arm, function() {});                              
            });
            focus.find("#control-ptz-focus").on("input",function() {
                const arm= parseInt(this.value);
                self.sendReq('ptz_focus', arm, function() {});                              
            });
            $('#control-jog-custom').append(focus);
            
            let ircut = $('<div class="jog-panel"><h1>IRCut</h1><button class="btn">ON</button></h1>')
            ircut.find('.btn').click(function() {
                
                if (this.innerText === "ON") {
                    self.sendReq("ptz_ircut", 1, function(){
                        ircut.find('.btn').text('OFF')
                    })
                } else {
                    self.sendReq("ptz_ircut", 0, function(){
                        ircut.find('.btn').text('ON')
                    })
                }
            })
            $('#control-jog-custom').append(ircut);

            setTimeout(() => {
                $.ajax({
                    url: "plugin/arducamfocus/ptz_inquire",
                    type: "GET",
                    dataType: "text",
                    success: function(c) {
                        switch (c) {
                            case "0":
                                $('#control-til-pan button').each(function() {console.log($(this).attr('disabled',true))})
                                ircut.find('.btn').attr('disabled',true);
                                $('#control-ptz-zoom').attr('disabled', true);
                                $('#control-ptz-focus').attr('max', 1023)
                                break; 
                            case "2":
                                $('#control-til-pan button').each(function() {console.log($(this).attr('disabled',true))})
                                $('#control-ptz-zoom').attr('disabled', true);
                                $('#control-ptz-focus').attr('disabled', true);
                                ircut.find('.btn').attr('disabled',true);
                                break;
                            default:
                                break;
                        }
                    },
                    error: function() {
                        console.log("error ajax")
                    }
                });
            }, 1000);

            


        }

        self.getTime = function(){
            var date = new Date();
            var time = date.getTime();
            return time;
        }

        self.sendReq = function(key, value, fn) {
            $.ajax({
                url: "plugin/arducamfocus/"+key + "?value=" + value,
                type: "GET",
                dataType: "text",
                success: function(c) {
                     fn()
                     console.log("send ok")
                },
                error: function() {
                    console.log("error ajax")
                }
            });
        }

        self.changeServo = function(angle) {
            $.ajax({
                url: "plugin/arducamfocus/focus?value="+angle,
                type: "GET",
                dataType: "text",
                success: function(c) {
                     $("#success").text(c);
                },
                error: function() {
                    console.log("error ajax")
                }
            });
            // self.time=self.getTime()
        }


        
    }

    /* view model class, parameters for constructor, container to bind to
     * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
     * and a full list of the available options.
     */
    OCTOPRINT_VIEWMODELS.push({
        construct: ArducamfocusViewModel,
        // ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
        dependencies: [ "printerStateViewModel", "loginStateViewModel", "filesViewModel", "settingsViewModel" ],
        // Elements to bind to, e.g. #settings_plugin_arducamfocus, #tab_plugin_arducamfocus, ...
        elements: [ /* ... */ ]
    });
});
