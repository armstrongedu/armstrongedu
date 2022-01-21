//jQuery time
var current_fs, next_fs, previous_fs; //fieldsets
var left, opacity, scale; //fieldset properties which we will animate
var animating; //flag to prevent quick multi-click glitches
var cur_lesson_id = 0;
var cur_topic_id = 0;

function addLesson(element) {
    var new_fs = $(`
        <fieldset>
        <h2 class="fs-title">Add Lesson</h2>
        <h3 class="fs-subtitle">Add a lesson or Quit and save</h3>
        <input type="button" name="previous" class="previous action-button" value="Previous" />
        <input type="button" name="next" class="next action-button" value="Next" />
        <br><h4>Title</h4>
        <input type="text" name="lesson-${cur_lesson_id}-title" placeholder="Title" >
        <h4>Arabic Title</h4>
        <input type="text" name="lesson-${cur_lesson_id}-title_ar" placeholder="Arabic Title" >
        <h4>Summary</h4>
        <textarea name="lesson-${cur_lesson_id}-summary" placeholder="Summary"></textarea>
        <h4>Arabic Summary</h4>
        <textarea name="lesson-${cur_lesson_id}-summary_ar" placeholder="Summary Arabic"></textarea>
        <input type="submit" class="action-button" value="Save and Quit" />
        <input type="button" class="add-lesson action-button" value="Next Lesson" />
        <input type="button" class="add-topic action-button" value="Add Topic" />
        </fieldset>
    `);
    new_fs.insertAfter(element);
    return new_fs;
}

function addProgress(element) {
    var li = $(`<li>Lesson ${cur_lesson_id}</li>`)
    li.insertAfter(element);
}

function addTopic(element) {
    var new_fs = $(`
    <fieldset>
      <h2 class="fs-title">Pick Topic Type</h2>
      <h3 class="fs-subtitle">Pick a Topic or Quit and save</h3>
      <input type="button" name="previous" class="previous action-button" value="Previous" />
      <input type="button" name="next" class="next action-button" value="Next" />
      <input type="submit" class="action-button" value="Save and Quit" />
      <input type="button" class="add-text-topic action-button" value="Text Topic"/>
      <input type="button" class="add-embedded-topic action-button" value="Embedded Topic"/>
      <input type="button" class="add-video-topic action-button" value="Video Topic"/>
      <input type="button" class="add-mcq-quiz-topic action-button" value="MCQ Quiz Topic" />
      <input type="button" class="add-tf-quiz-topic action-button" value="TF Quiz Topic" />
    </fieldset>
    `);
    new_fs.insertAfter(element);
    return new_fs;
}

function addTopicText(element) {
    var new_fs = $(`
    <fieldset>
      <h2 class="fs-title">Add Text Topic</h2>
      <h3 class="fs-subtitle">Add a Text Topic or Quit and save</h3>
      <input type="button" name="previous" class="previous action-button" value="Previous" />
      <input type="button" name="next" class="next action-button" value="Next" />
      <input type="hidden" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-type" value="TEXT" >
      <br><h4>Title</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-title" placeholder="Title" >
      <h4>Arabic Title</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-title_ar" placeholder="Title Arabic" >
      <h4>Content</h4>
      <textarea name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-summary" placeholder="Text"></textarea>
      <h4>Arabic Content</h4>
      <textarea name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-summary_ar" placeholder="Text Arabic"></textarea>
      <input type="submit" class="action-button" value="Save and Quit" />
      <input type="button" class="add-lesson action-button" value="Next Lesson"/>
      <input type="button" class="add-topic action-button" value="Add Topic" />
    </fieldset>
    `);
    new_fs.insertAfter(element);
    return new_fs;
}

function addTopicVideo(element) {
    var new_fs = $(`
    <fieldset>
      <h2 class="fs-title">Add Video Topic</h2>
      <h3 class="fs-subtitle">Add a Video Topic or Quit and save</h3>
      <input type="button" name="previous" class="previous action-button" value="Previous" />
      <input type="button" name="next" class="next action-button" value="Next" />
      <input type="hidden" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-type" value="VIDEO" >
      <br><h4>Title</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-title" placeholder="Title" >
      <h4>Arabic Title</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-title_ar" placeholder="Title Arabic" >
      <h4>Video File</h4>
      <input type="file" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-video_file" placeholder="Video Iframe" >
      <h4>Arabic Video File</h4>
      <input type="file" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-video_file_ar" placeholder="Video Iframe Arabic" >
      <input type="submit" class="action-button" value="Save and Quit" />
      <input type="button" class="add-lesson action-button" value="Next Lesson"/>
      <input type="button" class="add-topic action-button" value="Add Topic" />
    </fieldset>
    `);
    new_fs.insertAfter(element);
    return new_fs;
}

function addTopicEmbedded(element) {
    var new_fs = $(`
    <fieldset>
      <h2 class="fs-title">Add Embedded Topic</h2>
      <h3 class="fs-subtitle">Add a Embedded Topic or Quit and save</h3>
      <input type="button" name="previous" class="previous action-button" value="Previous" />
      <input type="button" name="next" class="next action-button" value="Next" />
      <input type="hidden" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-type" value="GAME" >
      <br><h4>Title</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-title" placeholder="Title" >
      <h4>Arabic Title</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-title_ar" placeholder="Title Arabic" >
      <h4>Iframe</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-iframe" placeholder="Iframe" >
      <h4>Arabic Iframe</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-iframe_ar" placeholder="Iframe Arabic" >
      <input type="submit" class="action-button" value="Save and Quit" />
      <input type="button" class="add-lesson action-button" value="Next Lesson"/>
      <input type="button" class="add-topic action-button" value="Add Topic" />
    </fieldset>
    `);
    new_fs.insertAfter(element);
    return new_fs;
}

function addTopicMCQQuiz(element) {
    var new_fs = $(`
    <fieldset>
      <h2 class="fs-title">Add MCQ Quiz Topic</h2>
      <h3 class="fs-subtitle">Add a MCQ Quiz Topic or Quit and save</h3>
      <input type="button" name="previous" class="previous action-button" value="Previous" />
      <input type="button" name="next" class="next action-button" value="Next" />
      <input type="hidden" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-type" value="MCQ" >
      <br><h4>Question</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-question" placeholder="Question" >
      <h4>Arabic Question</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-question_ar" placeholder="Question Arabic" >
      <h4>Wrong Choices</h4>
      <textarea name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-wrong_choices" placeholder="Wrong Choice 1, Wrong Choice 2"></textarea>
      <h4>Arabic Wrong Choices</h4>
      <textarea name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-wrong_choices_ar" placeholder="Wrong Choice 1 Arabic, Wrong Choice 2 Arabic"></textarea>
      <h4>Correct Choice</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-correct_choice" placeholder="Correct Choice" >
      <h4>Arabic Correct Choice</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-correct_choice_ar" placeholder="Correct Choice Arabic" >
      <input type="submit" class="action-button" value="Save and Quit" />
      <input type="button" class="add-lesson action-button" value="Next Lesson"/>
      <input type="button" class="add-topic action-button" value="Add Topic" />
    </fieldset>
    `);
    new_fs.insertAfter(element);
    return new_fs;
}

function addTopicTFQuiz(element) {
    var new_fs = $(`
    <fieldset>
      <h2 class="fs-title">Add TF Quiz Topic</h2>
      <h3 class="fs-subtitle">Add a TF Quiz Topic or Quit and save</h3>
      <input type="button" name="previous" class="previous action-button" value="Previous" />
      <input type="button" name="next" class="next action-button" value="Next" />
      <input type="hidden" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-type" value="TF" >
      <br><h4>Question</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-question" placeholder="Question" >
      <h4>Arabic Question</h4>
      <input type="text" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-question_ar" placeholder="Question Arabic" >
      <h4>Answer</h4>
      <div style="display: flex;">
          <input type="checkbox" id="lesson-${cur_lesson_id}-topic-${cur_topic_id}-answer" name="lesson-${cur_lesson_id}-topic-${cur_topic_id}-answer" ="" style="width: 10%;/* display: flex; */margin-top: 6px;">
          <p style="padding: 0; margin: 0;">Answer is True?</p>
      </div>
      <input type="submit" class="action-button" value="Save and Quit" />
      <input type="button" class="add-lesson action-button" value="Next Lesson"/>
      <input type="button" class="add-topic action-button" value="Add Topic" />
    </fieldset>
    `);
    new_fs.insertAfter(element);
    return new_fs;
}

$(document).on('click', '.add-lesson', function() {
    cur_lesson_id += 1;
    cur_topic_id = 0;
	if(animating) return false;
	animating = true;
	current_fs = $(this).parent();
        next_fs = addLesson(current_fs);
        console.log(next_fs);


	//activate next step on progressbar using the index of next_fs
        prog_bar = $("#progressbar").children().last();
        addProgress(prog_bar);
	$("#progressbar li").eq(-2).addClass("active");

	//show the next fieldset
	next_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(document).on('click', '.add-topic', function() {
	if(animating) return false;
	animating = true;
	current_fs = $(this).parent();
        next_fs = addTopic(current_fs);
        console.log(next_fs);


	//show the next fieldset
	next_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(document).on('click', '.add-text-topic', function() {
    cur_topic_id += 1;
	if(animating) return false;
	animating = true;
	current_fs = $(this).parent();
        next_fs = addTopicText(current_fs);
        console.log(next_fs);

	//show the next fieldset
	next_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(document).on('click', '.add-video-topic', function() {
    cur_topic_id += 1;
	if(animating) return false;
	animating = true;
	current_fs = $(this).parent();
        next_fs = addTopicVideo(current_fs);
        console.log(next_fs);

	//show the next fieldset
	next_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(document).on('click', '.add-embedded-topic', function() {
    cur_topic_id += 1;
	if(animating) return false;
	animating = true;
	current_fs = $(this).parent();
        next_fs = addTopicEmbedded(current_fs);
        console.log(next_fs);

	//show the next fieldset
	next_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(document).on('click', '.add-mcq-quiz-topic', function() {
    cur_topic_id += 1;
	if(animating) return false;
	animating = true;
	current_fs = $(this).parent();
        next_fs = addTopicMCQQuiz(current_fs);
        console.log(next_fs);

	//show the next fieldset
	next_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(document).on('click', '.add-tf-quiz-topic', function() {
    cur_topic_id += 1;
	if(animating) return false;
	animating = true;
	current_fs = $(this).parent();
        next_fs = addTopicTFQuiz(current_fs);
        console.log(next_fs);

	//show the next fieldset
	next_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({
        'transform': 'scale('+scale+')',
        'position': 'absolute'
      });
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(document).on('click', '.next', function() {
	if(animating) return false;
	animating = true;

	current_fs = $(this).parent();
	next_fs = $(this).parent().next();


	//show the next fieldset
	next_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale current_fs down to 80%
			scale = 1 - (1 - now) * 0.2;
			//2. bring next_fs from the right(50%)
			left = (now * 50)+"%";
			//3. increase opacity of next_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'transform': 'scale('+scale+')'});
			next_fs.css({'left': left, 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});

$(document).on('click', '.previous', function() {
	if(animating) return false;
	animating = true;

	current_fs = $(this).parent();
	previous_fs = $(this).parent().prev();


	//show the previous fieldset
	previous_fs.show();
	//hide the current fieldset with style
	current_fs.animate({opacity: 0}, {
		step: function(now, mx) {
			//as the opacity of current_fs reduces to 0 - stored in "now"
			//1. scale previous_fs from 80% to 100%
			scale = 0.8 + (1 - now) * 0.2;
			//2. take current_fs to the right(50%) - from 0%
			left = ((1-now) * 50)+"%";
			//3. increase opacity of previous_fs to 1 as it moves in
			opacity = 1 - now;
			current_fs.css({'left': left});
			previous_fs.css({'transform': 'scale('+scale+')', 'opacity': opacity});
		},
		duration: 800,
		complete: function(){
			current_fs.hide();
			animating = false;
		},
		//this comes from the custom easing plugin
		easing: 'easeInOutBack'
	});
});
