var { spawn } = require('child_process');
var result_02 = spawn('python', ['function.py', 'minju', '26'])
// const result_01 = spawn('python', ['./handKeyPointDetection/blurFinger.py', firstPhoto]);

// result_01.stdout.on('data', (result)=> {
// 	console.log(result);
// 	resultPhoto = result;
// }); 

result_02.stdout.on('data', (result)=> {
	console.log(result.toString());
});