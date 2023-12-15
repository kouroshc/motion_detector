$(document).ready(function () {
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
    var timeFrame = $("#timeFrame").val()
    $("#timeFrame").change(function () {
        $("#timeFrameValue").html(`${$("#timeFrame").val()}`)
    })

    //VIdeo
    // const video = document.getElementById('video');
    // navigator.mediaDevices.enumerateDevices()
    //     .then(devices => {
    //         const videoDevices = devices.filter(device => device.kind === 'videoinput');
    //         const videoDeviceIds = videoDevices.map(device => device.deviceId);
    //         const videoConstraints = {video: {deviceId: videoDeviceIds[0]}};
    //         return navigator.mediaDevices.getUserMedia(videoConstraints);
    //     })
    //     .then(stream => {
    //         video.srcObject = stream;
    //     })
    //     .catch(error => {
    //         console.error(error);
    //     });

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
        stopRecording(theStream);

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
        //theRecorderStream.cancel();
    }

    $("#record-button").click(function () {
        var constraints = {video: true, audio: true};

        if (theStream) {
            if (theRecorder.state == 'recording' && theRecorder.state) {
                stopRecording(theStream);
                console.log("Second record", theRecorder)
            }
        } else {
            getUserMedia(constraints, function (stream) {
                var mediaControl = document.querySelector('video');
                console.log(mediaControl)


                if (navigator.mozGetUserMedia) {
                    mediaControl.mozSrcObject = stream;
                } else {
                    mediaControl.srcObject = stream;
                }

                theStream = stream;
                try {
                    recorder = new MediaRecorder(stream);
                } catch (e) {
                    console.error('Exception while creating MediaRecorder: ' + e);
                    return;
                }
                theRecorder = recorder;
                console.log('MediaRecorder created');
                recorder.ondataavailable = recorderOnDataAvailable;
                recorder.start(100);
            }, function (err) {
                alert('Error: ' + err);
            });
        }
    });

    function recorderOnDataAvailable(event) {
        if (event.data.size == 0) return;
        console.log('ondataavailable, type: ' + event.data.type);
        recordedChunks.push(event.data);
        console.log(recordedChunks);
    }

    $("#stop-button").click(function () {
        saveRecording();
    });


    //Result
    setInterval(() => {
        $.ajax({
            url: 'static/scripts/result.json',
            dataType: 'json',
            success: (animationData) => {
                $("#result-container").html(animationData.svg);
            }
        });
    }, timeFrame);
//Record BTN
    var isRecording = false;
    var timerInterval;

    $('#record-button').click(function () {
        if (isRecording) {
            clearInterval(timerInterval);
            $('#record-button').removeClass('recording');
            $('#timer').text('');
        } else {
            var startTime = Date.now();
            timerInterval = setInterval(function () {
                var elapsedTime = Date.now() - startTime;
                var minutes = Math.floor(elapsedTime / 60000);
                var seconds = ((elapsedTime % 60000) / 1000).toFixed(0);
                $('#timer').text(minutes + ':' + (seconds < 10 ? '0' : '') + seconds);
            }, 1000);
            $('#record-button').addClass('recording');
        }
        isRecording = !isRecording;
    });


//    Table

//    Slider

    setInterval(function () {
        $.getJSON("static/scripts/test.json", function (data) {
            $(".statisticsTableTbody").empty();
            for (let item of data.table) {
                $(".statisticsTableTbody").append(`
            <tr class="${item.category}">
                    <td>${item.body}</td>
                    <td>
                        <label class="sliderLabel">${item.degree}°</label>
                        <input type="range" min="-180" max="180"
                               value="${item.degree}" class="slider" smooth=yes disabled >
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

//    Standards
    setInterval(function () {
        $.getJSON("static/scripts/test.json", function (data) {
            $(".score").empty();
            for (let item of data.standards) {

                $(".score").append(`
            <div class="scoreNo ">${item.standarsNo}</div>
                    <div class="scoreResult ">${item.standarsScore}</div>
            `)
            }
        });
    }, 1000);


})
;