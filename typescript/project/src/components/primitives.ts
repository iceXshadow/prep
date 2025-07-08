// TypeScript Primitives - Notes with Examples

// 1. Number
// You can declare a variable as a number explicitly or implicitly.

let x: number = 2; // Explicit number type
let y = 3;         // Implicitly inferred as number

console.log(x, y); // Output: 2 3

// 2. String
// Declare a variable as a string and assign values.

let z: string;

z = "hello";
z = "3";
z = `${y}`; // Using template literals

// 3. Boolean
// Example of a boolean variable.

let isActive: boolean = true;
console.log(isActive)

// 4. Null and Undefined
// null: Explicitly means "no value" or "empty".
// undefined: Variable declared but not assigned a value.

let res: null = null;           // Explicitly set to null
console.log(res);
let dres: undefined = undefined; // Explicitly set to undefined
console.log(dres)

// 5. Union Types
// A variable can have more than one type.

let ans: number | undefined = undefined; // Can be number or undefined
ans = 2; // Later assigned a number

// 6. Void
// Used for functions that do not return a value.

function logMessage(message: string): void {
    console.log(message);
}

logMessage("This is a log message."); // Example usage to avoid unused variable warning

// 7. Never
// Used for functions that never return (e.g., throw an error or infinite loop).

function throwError(message: string): never {
    throw new Error(message);
}

throwError("This is an error: this code is never to be reached!")

// Summary of Primitive Types in TypeScript:
// - number
// - string
// - boolean
// - undefined
// - null
// - void
// - never