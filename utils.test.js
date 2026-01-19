const assert = require('assert');
const { addNumbers, subtractNumbers } = require('./utils.js');

function testAddNumbers() {
  const result = addNumbers(2, 3);
  assert.strictEqual(result, 5, 'Test Case 1 Failed: 2 + 3 should be 5');
  console.log('Test Case 1 Passed!');
}

function testAddNumbersWithNegative() {
  const result = addNumbers(-5, 5);
  assert.strictEqual(result, 0, 'Test Case 2 Failed: -5 + 5 should be 0');
  console.log('Test Case 2 Passed!');
}

function testSubtractNumbers() {
  const result = subtractNumbers(5, 2);
  assert.strictEqual(result, 3, 'Test Case 3 Failed: 5 - 2 should be 3');
  console.log('Test Case 3 Passed!');
}

try {
  testAddNumbers();
  testAddNumbersWithNegative();
  testSubtractNumbers();
  console.log('All tests passed for utils.js!');
} catch (error) {
  console.error(error.message);
  process.exit(1);
}
