// Logging support functions

function logTrial(worker, trial, session, frametime, speed, starttime, duration, avrgproximity, misses, numtargets, targetshit, targetsmissed, retry) {
  retry = (typeof retry === 'undefined') ? 3 : retry;
  $.ajax({
    url: "php/log_trial.php",
    data: {worker: worker, trial: trial, session: session, frametime: frametime, speed: speed, starttime: starttime, duration: duration, avrgproximity: avrgproximity, misses:misses, numtargets: numtargets, targetshit: targetshit, targetsmissed: targetsmissed},
    dataType: "text",
    success: function(d) {
      //
    },
    error: function(d) {
      if (retry > 0) {
        logTrial(worker, trial, session, frametime, speed, starttime, duration, avrgproximity, misses, numtargets, targetshit, targetsmissed, retry-1);
      }
    }
  });
}

function logTarget(worker, trial, session, frametime, speed, targetindex, starttime, duration, startloc, endloc, path, distance, proximity, misses, retry) {
  retry = (typeof retry === 'undefined') ? 3 : retry;
  $.ajax({
    url: "php/log_target.php",
    data: {worker: worker, trial: trial, session: session, frametime: frametime, speed: speed, targetindex: targetindex, starttime: starttime, duration: duration, startloc: startloc, endloc: endloc, path: path, distance: distance, proximity: proximity, misses: misses},
    dataType: "text",
    success: function(d) {
      //
    },
    error: function(d) {
      if (retry > 0) {
        logTarget(worker, trial, session, frametime, speed, targetindex, starttime, duration, startloc, endloc, path, distance, proximity, misses, retry-1);
      }

    }
  });
}



