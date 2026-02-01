# sm_blueprint_lib

A powerful Python library for programmatically creating and manipulating Scrap Mechanic blueprints. Build complex logic circuits, automated systems, and mechanical constructions with code instead of manual placement.

## 🚀 Features

- **Programmatic Blueprint Creation**: Design blueprints using Python code
- **Logic Circuit Support**: Create complex logic gates and connections
- **Performance Optimized**: Fast iterative algorithms and caching
- **3D Preview**: Visualize your creations before importing
- **Pre-built Components**: Ready-to-use logic circuits (adders, counters, RAM, etc.)
- **Flexible Positioning**: Precise control over part placement and rotation
- **Color System**: Support for hex colors, RGB tuples, and paint gun colors

## 📦 Installation

```bash
pip install sm_blueprint_lib
```

### Dependencies

- numpy >= 2.4.1
- pygame >= 2.6.1 (for preview functionality)
- moderngl >= 5.12.0 (for preview functionality)
- pyglm >= 2.8.3 (for preview functionality)
- PyWavefront >= 1.3.3 (for preview functionality)

## 🛠 Quick Start

```python
import sm_blueprint_lib as sm

# Create a new blueprint
bp = sm.Blueprint()

# Create a logic gate
gate = sm.LogicGate(pos=(0, 0, 0), color="1122ff", controller=0)

# Add it to the blueprint
bp.add(gate)

# Save the blueprint
sm.save_blueprint("my_blueprint", bp)
```

## 📖 Core Concepts

### Parts and Components

The library provides various parts you can use:

```python
# Logic gates with different modes
and_gate = sm.LogicGate((0, 0, 0), "ffffff", "and")      # AND gate
or_gate = sm.LogicGate((1, 0, 0), "ffffff", "or")        # OR gate
xor_gate = sm.LogicGate((2, 0, 0), "ffffff", "xor")      # XOR gate

# Timers and sensors
timer = sm.Timer((0, 1, 0), "3210ff", (1, 0))           # 1 second timer
sensor = sm.Sensor((0, 2, 0), "ff0000")                  # Sensor

# Mechanical parts
piston = sm.Piston((0, 3, 0), "888888")                 # Piston
bearing = sm.Bearing((0, 4, 0), "666666")               # Bearing
```

### Controller Modes

Logic gates support multiple controller modes:

```python
# Numeric modes
sm.LogicGate(pos=(0, 0, 0), color="ffffff", controller=0)  # AND
sm.LogicGate(pos=(0, 0, 0), color="ffffff", controller=1)  # OR
sm.LogicGate(pos=(0, 0, 0), color="ffffff", controller=2)  # XOR
sm.LogicGate(pos=(0, 0, 0), color="ffffff", controller=3)  # NAND
sm.LogicGate(pos=(0, 0, 0), color="ffffff", controller=4)  # NOR
sm.LogicGate(pos=(0, 0, 0), color="ffffff", controller=5)  # XNOR

# String modes
sm.LogicGate(pos=(0, 0, 0), color="ffffff", controller="and")
sm.LogicGate(pos=(0, 0, 0), color="ffffff", controller="or")
```

### Color System

Multiple color formats are supported:

```python
# Hex colors
gate1 = sm.LogicGate((0, 0, 0), "1122ff", 0)
gate2 = sm.LogicGate((1, 0, 0), "#FF5733", 1)

# RGB tuples
gate3 = sm.LogicGate((2, 0, 0), (255, 87, 51), 2)

# Paint gun colors
gate4 = sm.LogicGate((3, 0, 0), sm.PAINT_COLOR.Yellow, 3)
gate5 = sm.LogicGate((4, 0, 0), sm.PAINT_COLOR.Barberry, 4)
```

## 🔗 Connections

The library provides flexible connection patterns:

### 1-to-1 Connections
```python
sm.connect(gate1, gate2)
```

### 1-to-Many Connections
```python
row = [sm.LogicGate((x, 1, 0), "ffffff", 0) for x in range(5)]
sm.connect(input_gate, row)
```

### Many-to-1 Connections
```python
sm.connect(row, output_gate)
```

### Many-to-Many Connections
```python
row1 = [sm.LogicGate((x, 2, 0), "ffffff", 0) for x in range(5)]
row2 = [sm.LogicGate((x, 3, 0), "ffffff", 1) for x in range(5)]

# Parallel connections (row-to-row)
sm.connect(row1, row2, parallel=True)

# Cross connections (everything to everything)
sm.connect(row1, row2, parallel=False)
```

### Chained Connections
```python
# Chain multiple connections
gate1.connect(gate2).connect(gate3).connect(gate1)
```

## 🏗 Advanced Usage

### Creating Complex Structures

```python
import numpy as np

# Create a 10x10 logic gate matrix
matrix = np.ndarray((10, 10), dtype=sm.LogicGate)
for x in range(10):
    for z in range(10):
        matrix[x, z] = sm.LogicGate(
            (x, 8, z + 1), "000000", 5, xaxis=1, zaxis=2
        )

# Add multiple components at once
bp.add(
    matrix,                    # 2D array
    row1, row2,               # Lists
    single_gate,              # Single part
    nested_structure          # Nested lists
)
```

### Custom Controllers

```python
# Create a controller with custom settings
custom_controller = sm.LogicGateController(
    mode=2,                    # XOR mode
    id=9999999,               # Custom ID
    controllers=[sm.ID(9999999)]  # Self-reference
)

gate = sm.LogicGate(
    pos=(0, 0, 0),
    color="5522ff",
    controller=custom_controller
)
```

### Rotation and Positioning

```python
# Custom rotation (xaxis, zaxis)
gate = sm.LogicGate(
    (x, y, z), "000000", 5, 
    xaxis=1,    # X-axis rotation
    zaxis=2     # Z-axis rotation
)

# Use Position objects
pos = sm.Pos(10, 5, 3)
gate = sm.LogicGate(pos, "ffffff", 0)
```

## 📦 Pre-built Components

The library includes pre-built logic circuits:

```python
# 4-bit adder
adder = sm.adder(bp, bit_length=4, pos=(0, 0, 0))

# 8-bit counter
counter = sm.counter(bp, bit_length=8, pos=(10, 0, 0))

# RAM module
ram = sm.ram(bp, bit_length=8, num_address=16, pos=(20, 0, 0))

# Timer-based system
timer_ram = sm.timer_ram_cached(bp, bit_length=4, num_address=8, pos=(30, 0, 0))
```

## 👁 3D Preview

Visualize your blueprints before importing:

```python
# Preview your blueprint in 3D
sm.preview(bp)

# The preview window supports:
# - Mouse drag to rotate view
# - Scroll to zoom
# - WASD keys to move camera
# - Q/E keys to move up/down
```

## 💾 Saving and Loading

### Save Blueprints
```python
# Save as new blueprint
sm.make_new_blueprint("my_awesome_circuit", bp)

# Overwrite existing blueprint
sm.save_blueprint("existing_blueprint", bp)

# Export as JSON string
json_data = sm.dump_string_from_blueprint(bp)
print(json_data)
```

### Load Blueprints
```python
# Load from file
loaded_bp = sm.load_blueprint("path/to/blueprint.json")

# Load from JSON string
loaded_bp = sm.load_blueprint_from_string(json_data)
```

## 🎯 Example Projects

### Simple Logic Circuit
```python
import sm_blueprint_lib as sm

# Create blueprint
bp = sm.Blueprint()

# Create basic gates
input_a = sm.LogicGate((0, 0, 0), "ff0000", 0)  # AND gate
input_b = sm.LogicGate((1, 0, 0), "00ff00", 0)  # AND gate
output = sm.LogicGate((2, 0, 0), "0000ff", 1)   # OR gate

# Connect them
sm.connect(input_a, output)
sm.connect(input_b, output)

# Add to blueprint and save
bp.add(input_a, input_b, output)
sm.save_blueprint("simple_logic", bp)
```

### Timer Loop
```python
# Create a timing circuit
loop = [
    sm.LogicGate((4, 0, 0), "987654"),                    # Logic gate
    sm.Timer((5, 0, 0), "3210ff", (1, 0)),               # 1-second timer
    sm.LogicGate((6, 0, 0), "eeddcc", 3)                 # NAND gate
]

# Chain them together
loop[0].connect(loop[1]).connect(loop[2]).connect(loop[0])

bp.add(loop)
sm.save_blueprint("timer_loop", bp)
```

## 🚀 Performance

The library is optimized for performance:

- **Iterative Algorithms**: No recursion limits for large structures
- **Efficient Connections**: Batch operations for complex wiring
- **Path Caching**: Fast repeated file operations
- **Lazy Loading**: Preview components loaded only when needed

## 📚 API Reference

### Core Classes

- **`Blueprint`**: Main container for parts and bodies
- **`LogicGate`**: Logic gate components
- **`Timer`**: Timer components
- **`Sensor`**: Sensor components
- **`Pos`**: Position objects

### Utility Functions

- **`connect()`**: Connect parts together
- **`save_blueprint()`**: Save blueprint to file
- **`load_blueprint()`**: Load blueprint from file
- **`dump_string_from_blueprint()`**: Export as JSON
- **`preview()`**: Show 3D preview

### Constants

- **`PAINT_COLOR`**: Available paint colors
- **`SHAPEID`**: Part shape identifiers
- **`BLOCKS`**: Block type names

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/MauriceTZ/sm_blueprint_lib)
- [Issue Tracker](https://github.com/MauriceTZ/sm_blueprint_lib/issues)
- [PyPI Package](https://pypi.org/project/sm-blueprint-lib/)

---

## 🖼 Examples

### Logic Gate Matrix
![Logic Gate Matrix](rowtorowand1tomany.png)

### Complex Connections
![Complex Connections](manytooneandmanytomany.png)

### Timer Circuit
![Timer Circuit](1to1andloop.png)
