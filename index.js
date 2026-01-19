const _ = require('lodash');
const { addNumbers, subtractNumbers } = require('./utils');

console.log("Hello from the dev branch! Current time: " + new Date().toLocaleString());
console.log("The sum of 5 and 3 is: " + addNumbers(5, 3));
console.log("The difference of 20 and 10 is: " + subtractNumbers(20, 10));
console.log("The sum of [1, 2, 3, 4, 5] using lodash is: " + _.sum([1, 2, 3, 4, 5]));