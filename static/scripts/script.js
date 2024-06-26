$(document).ready(function () {

                    $('#result_annotated').hide()
//    Menu
        $("a#pageLink").click(function () {
            $("a#pageLink").removeClass("active");
            $(this).addClass("active");
        });

        $(".btn-show-left-area").click(function () {
            $(".left-area").toggleClass("show");
            // $(".left-area").addClass("show");
        });

        $(".btn-show-right-area").click(function () {
            $(".right-area").removeClass("show");
            $(".right-area").addClass("show");
        });

        $(".btn-close-right").click(function () {
            $(".right-area").removeClass("show");
        });

        $(".btn-close-left").click(function () {
            $(".left-area").removeClass("show");
        });
//     TimeFrame
        var timeFrame = $("#timeFrameValue").html()
        timeFrame *= 1000
    console.log(navigator.webkitGetUserMedia)
        // $("#timeFrame").change(function () {
        //     $("#timeFrameValue").html(`${$("#timeFrame").val()}`)
        // })

     navigator.mediaDevices.enumerateDevices().then(function (devices) {
            for(var i = 0; i < devices.length; i ++){
                var device = devices[i];
                if (device.kind === 'videoinput') {
                    var option = document.createElement('option');
                    option.value = device.deviceId;
                    option.text = device.label || 'camera ' + (i + 1);
                    document.querySelector('select#videoSource').appendChild(option);
                }
            };
        });


        function getUserMedia(options, successCallback, failureCallback) {
            var api = navigator.getUserMedia || navigator.webkitGetUserMedia ||
                navigator.mozGetUserMedia || navigator.msGetUserMedia;
            if (api) {
                return api.bind(navigator)(options, successCallback, failureCallback);
            }
            alert('User Media API not supported.');
        }

        var theStream;
        var theRecorder;
        var recordedChunks = [];

        function saveRecording() {
            console.log('Saving data');
            theRecorder.stop();
            theRecorder.onstop = recorderOnStop();

            // stopRecording(theStream);

            var blob = new Blob(recordedChunks, {type: "video/webm"});
            var url = (window.URL || window.webkitURL).createObjectURL(blob);
            var a = document.createElement("a");
            document.body.appendChild(a);
            a.style = "display: none";
            a.href = url;
            a.download = 'test.webm';
            a.click();

            // setTimeout() here is needed for Firefox.
            setTimeout(function () {
                (window.URL || window.webkitURL).revokeObjectURL(url);
            }, 100);
        }

        function stopRecording(theMediaStream) {
            theMediaStream.getTracks().forEach((track) => {
                track.stop();
            })
        };

        $("#record-button").click(function () {
                var constraints = {video: true, audio: false};

                if (theStream) {
                    if (theRecorder.state == 'recording' && theRecorder.state) {
                        theRecorder.pause();
                        theRecorder.onpause = recorderOnPause();

                    } else if (theRecorder.state == 'paused' && theRecorder.state) {
                        theRecorder.resume();
                        theRecorder.onresume = recorderOnResume();
                        // console.log("resume", theRecorder)
                    }


                } else {
                    getUserMedia(constraints, function (stream) {
                        var mediaControl = document.querySelector('video');
                        if (navigator.mozGetUserMedia) {
                            mediaControl.mozSrcObject = stream;
                        } else {
                            mediaControl.srcObject = stream;
                        }
                        theStream = stream;
                        console.log(theStream)
                        try {
                            recorder = new MediaRecorder(stream);
                            recorder.onstart = recorderOnStart;

                        } catch (e) {
                            console.error('Exception while creating MediaRecorder: ' + e);
                            return;
                        }
                        theRecorder = recorder;
                        console.log(recorder)

                        console.log('MediaRecorder created');

                        recorder.ondataavailable = recorderOnDataAvailable;
                        recorder.start(100);
                    }, function (err) {
                        alert('Error: ' + err);
                    });
                }
            }
        )
        ;

        var startTime;
        var pauseTime;
        var timerInterval;

        function recorderOnStart(event) {
            console.log("started")
            console.log(theRecorder.state)
            startTime = Date.now();
            recordingTimer(startTime, theRecorder.state)

        }

        function recorderOnPause(event) {
            console.log("Paused")
            console.log(theRecorder.state)
            pauseTime = Date.now();
            recordingTimer(startTime, theRecorder.state)

        }

        function recorderOnStop(event) {
            theStream = null;
            // theRecorder = null;
            console.log("Stoped")
            console.log(theRecorder.state)
            recordingTimer(startTime, theRecorder.state)
        }

        function recorderOnResume(event) {
            console.log("Resumed")
            console.log(theRecorder.state)
            startTime += Date.now() - pauseTime;
            recordingTimer(startTime, theRecorder.state)
        }

        function recordingTimer(startTime, status) {

            if (status == 'recording') {
                timerInterval = setInterval(function () {
                    var elapsedTime = Date.now() - startTime;
                    var minutes = Math.floor(elapsedTime / 60000);
                    var seconds = ((elapsedTime % 60000) / 1000).toFixed(0);
                    $('#timer').text(minutes + ':' + (seconds < 10 ? '0' : '') + seconds);
                    console.log(minutes + ':' + (seconds < 10 ? '0' : '') + seconds)
                }, 1000);
                $('#record-button').addClass('recording');
            }
            if (status == 'inactive') {
                clearInterval(timerInterval);
                $('#record-button').removeClass('recording');
                $('#timer').text('');
            }
            if (status == 'paused') {
                clearInterval(timerInterval);
            }

        }


        function recorderOnDataAvailable(event) {
            if (event.data.size == 0) return;
            recordedChunks.push(event.data);
        }

        $("#stop-button").click(function () {
            saveRecording();
        });


        // setInterval(() => {
        //     $.ajax({
        //         url: 'static/scripts/result.json',
        //         dataType: 'json',
        //         success: (animationData) => {
        //             $("#result-container").html(animationData.svg);
        //         }
        //     });
        // }, timeFrame);


//    Table

//    Slider


        setInterval(function () {
            $.getJSON("static/scripts/data.json", function (data) {
                $(".statisticsTableTbody").empty();
                for (let item of data.Body_Angles) {
                    $(".statisticsTableTbody").append(`
            <tr class="${item.category}">
                    <td>${item.part}</td>
                    <td>
                        <label class="sliderLabel">${item.angle}°</label>
                        <input type="range" min="0" max="360" step="0.1"
                               value="${item.angle}" class="slider" smooth=yes disabled >
                    </td>
                </tr>
            `)
                }
            });
        }, timeFrame);
//statistics
        //Init
        $(".score").hide(200);
        $(".charts").hide(200);
        $(".charts").show(200);
        $("#tabsChart").addClass("active");
        $("#tabsStandars").removeClass("active");
        $("#tabsChart").click(function () {
            $(".score").hide(200);
            $(".charts").hide(200);
            $(".charts").show(200);
            $("#tabsChart").addClass("active");
            $("#tabsStandars").removeClass("active");

        });
        $("#tabsStandars").click(function () {
            $(".score").hide(200);
            $(".charts").hide(200);
            $(".score").show(200);
            $("#tabsStandars").addClass("active");
            $("#tabsChart").removeClass("active");

        });
            let i = 0;

        $('#nodesDisplay').click(function (){
            i++;
            console.log(i)
            if (i % 2 == 0){
                    $('#camera_video').hide()
                    $('#result_annotated').show()}
            if (i % 2 == 1){
                    $('#camera_video').show()
                    $('#result_annotated').hide()}
        })

//    Standards
//         setInterval(function () {
//             $.getJSON("static/scripts/data.json", function (data) {
//                 $(".score").empty();
//                 for (let item of data.standards) {
//
//                     $(".score").append(`
//             <div class="scoreNo ">${item.standarsNo}</div>
//                     <div class="scoreResult ">${item.standarsScore}</div>
//             `)
//                 }
//             });
//         }, 1000);
//         setInterval(function () {
//             $.getJSON("static/scripts/data.json", function (data) {
//                 $(".score").empty();
//                 for (let item of data.standards) {
//
//                     $(".score").append(`
//             <div class="scoreNo ">${item.standarsNo}</div>
//                     <div class="scoreResult ">${item.standarsScore}</div>
//             `)
//                 }
//             });
//         }, 1000);


    }
);