function changeGrade(row_id, action) {
	var row = $('#' + row_id);
	var score = row.children(':nth-child(2)');
	var message = row.children(':nth-child(4)');
	var actions = row.children(':nth-child(5)');

	if(action == 'edit') {
		score.data('oldScore', score.html());
		message.data('oldMessage', message.html());

		var val = score.html();
		if(val == '‒') {
			val = '-1';
		}

		score.html('<input type="text" value="' + val + '">');
		message.html('<input type="text" value="' + message.html() + '">');
		actions.html('<a href="javascript:changeGrade(\'' + row_id + '\', \'save\')">save</a> <a href="javascript:changeGrade(\'' + row_id + '\', \'reset\')">cancel</a>');
	} else if(action == 'reset') {
		score.html(score.data('oldScore'));
		message.html(message.data('oldMessage'));
		actions.html('<a href="javascript:changeGrade(\'' + row_id + '\', \'edit\')">edit</a>');
	} else if(action == 'save') {
		// TODO
	}
}

$(function() {
	if($("#username").length) {
		$("#username").focus();
	}
});
