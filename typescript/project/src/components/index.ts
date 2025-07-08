// ===============================
// Arrays and Tuples in TypeScript
// ===============================

// Arrays ->
// It's best practice to store only one type of data in an array for type safety.

// Example 1: Array of numbers
const numbers: number[] = [1, 2, 3, 4, 5];
console.log(numbers);

// Example 2: Array of strings
const fruits: string[] = ["apple", "banana", "cherry"];
console.log(fruits);

// Example 3: Array of booleans
const flags: boolean[] = [true, false, true, false];
console.log(flags);

// Example 4: Array of objects
interface User {
    id: number;
    name: string;
}


const users: User[] = [
    { id: 1, name: "Alice" },
    { id: 2, name: "Bob" }
];
console.log(users);

// Example 5: Multi-dimensional array (array of arrays)
const matrix: number[][] = [
    [1, 2],
    [3, 4],
    [5, 6]
];
console.log(matrix)


// Tuples

// A tuple is a fixed-length array where each element can have a different type.
// The order and types of elements are strictly defined.

// Example 1: Tuple with two elements (number, string)
const userTuple: [number, string] = [1, "Alice"];
console.log(userTuple);

// Example 2: Tuple with three elements (string, number, boolean)
const productTuple: [string, number, boolean] = ["Book", 29.99, true];
console.log(productTuple);

// Example 3: Tuple representing RGB color (number, number, number)
const rgb: [number, number, number] = [255, 0, 128];
console.log(rgb);

// Example 4: Tuple with optional elements
const optionalTuple: [string, number?] = ["optional"];
console.log(optionalTuple)

// Example 5: Array of tuples (useful for coordinates, key-value pairs, etc.)
const coordinates: [number, number][] = [
    [10, 20],
    [30, 40],
    [50, 60]
];

// Accessing tuple elements
const firstCoord = coordinates[0]; // [10, 20]
const x = firstCoord[0]; // 10
const y = firstCoord[1]; // 20

console.log(x);
console.log(y);


// Notes

// - Arrays should be homogeneous (same type).
// - Tuples are useful when you want to group a fixed number of elements of different types.
// - TypeScript enforces the types and order in tuples, providing better type safety.

// Literals & Enums

// literals are instances of primitives

// where we know we are going to be handling only a select amount of different values
let direction: "north" | "south" | "east" | "west";
direction = "north"

if (direction === "north") console.log(direction);

let resCode: 200 | 201 | 404;

resCode = 200;

// enums enables developers to estabilish a collection named constants (enumerators) each linked to an integer value

// numeric enums

// using enums we can map text to integer values and use them throughout the code interchangibly
enum Size { // automatic mapping is also done
    Small = 0,
    Medium = 5,
    Large = 10
}
//This syntax is not allowed when 'erasableSyntaxOnly' is enabled.ts(1294) -> this interesting error occured cuz the enum leaves artifacts at run time and it is not erased...

var size: Size = Size.Small;

if (size === 0) {
    // do something
}

// string enums
enum Direction {
    North = "NORTH",
    South = "SOUTH",
    East = "EAST",
    West = "WEST"
}

let dir: Direction = Direction.North;
if (dir === Direction.North) {
    console.log("Heading North");
}