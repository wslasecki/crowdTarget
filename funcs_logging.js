// Logging support functions

function logTrial(worker, trial, session, frametime, speed, starttime, duration, avrgproximity, misses, targetsmissed) {
  $.ajax({
    url: "log_trial.php",
    data: {worker: worker, trial: trial, session: session, frametime: frametime, speed: speed, starttime: starttime, duration: duration, avrgproximity: avrgproximity, misses:misses, targetsmissed: targetsmissed},
    dataType: "text",
    success: function(d) {
      //
    }
  });
}

function logTarget(worker, trial, session, frametime, speed, targetindex, starttime, duration, startloc, endloc, path, distance, proximity, misses) {
  $.ajax({
    url: "log_target.php",
    data: {worker: worker, trial: trial, session: session, frametime: frametime, speed: speed, targetindex: targetindex, starttime: starttime, duration: duration, startloc: startloc, endloc: endloc, path: path, distance: distance, proximity: proximity, misses: misses},
    dataType: "text",
    success: function(d) {
      //
    }
  });
}



