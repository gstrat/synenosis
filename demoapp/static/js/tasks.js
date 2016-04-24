(function($) {
	// callback is an optional function to call once the task has finished
	// instead of the classic markusertaskfinished call
	$.askProgress = function(job_id, progresswrapper, task_name, timer, callback) {
		if (!progresswrapper.data('asking')) {
			progresswrapper.data('asking', true);
			$.get('/task-progress/', 'job='+job_id, function(data) {
				var progressholder = progresswrapper.find('div.progress-bar');
				progresswrapper.find('p').html(data.message);
				if (data.error) {
					progressholder.width(0 + "%").find("span").html(0 + "%");
					progresswrapper.data('asking', false);
				} else {
					progressholder.width(data.progress + "%").find("span").html(data.progress + "%");
					progresswrapper.data('asking', false);
					if (parseInt(data.progress) == 100) {
						window.clearInterval(timer);
						progresswrapper.html('');
						window.location = '/';
					}
				}
			}, 'json');
		}
	}

	$.initTask = function(job_id, task_name, title, message, progress) {
		//Make a loader.
		var progresswrapper = $('#progress-wrapper')
		progresswrapper.append(
			'<div class="progress progress-striped active" style="height: 30px">\
						<div class="progress-bar progress-bar-success" role="progressbar" style="width: ' + progress + '%">\
							<span class="sr-only">' + progress + '%</span>\
						</div>\
					</div>\
					<p>'+message+'</p>');

		var timer = setInterval(function() {
				$.askProgress(job_id, progresswrapper, task_name, timer);
			}, 600);
		$.askProgress(job_id, progresswrapper, task_name, timer);
	};

	$(document).ready(function() {
		$('a.run-job').on('click', function(data) {
			$this = $(this);
			//init job
			var datastring = $this.closest('form').serialize();
			$.ajax({
			    type: "POST",
			    url: $this.attr('href'),
			    data: datastring,
			    dataType: "json",
			    success: function(data) {
			    	$.initTask(data.job_id, data.task_name, $this.data('title'),
							data.message, data.progress);
			    }
			});
			return false;
		});
	})
})(jQuery);