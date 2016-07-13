/* 
* @Author: mustafa
* @Date:   2015-08-01 06:45:50
* @Last Modified by:   mustafa
* @Last Modified time: 2015-08-01 07:53:48
*/

'use strict';
var trim = function (string) {
	return string.toString().replace(/^\s+/, '').replace(/\s+$/, '');
};

exports.new = function(control) {
	var splitted = control.split("\n"),
		res = {};

	for(var i = 0; i < splitted.length; i++){
		var line = splitted[i],
			type = trim(line.substring(0, line.indexOf(":"))),
			value = trim(line.substring(line.indexOf(":")+1, line.length));

		res[type] = value;
	}

	return res;
}

exports.toControl = function(control) {
	if (typeof control != 'object') return "error";
	var res = "";

	for (var key in control) {
		if (control.hasOwnProperty(key)) {
			if (key != "") {
				res += key + ": " + control[key] + "\n";
			}
		}
	}

	return res;
}