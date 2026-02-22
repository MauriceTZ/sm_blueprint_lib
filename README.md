# sm_blueprint_lib

[![PyPI version](https://img.shields.io/pypi/v/sm_blueprint_lib.svg)](https://pypi.org/project/sm_blueprint_lib/)
[![Python versions](https://img.shields.io/pypi/pyversions/sm_blueprint_lib.svg)](https://pypi.org/project/sm_blueprint_lib/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A powerful Python library for creating, manipulating, and previewing **Scrap Mechanic** blueprints programmatically. This library provides a comprehensive API for building complex logic circuits, mechanical systems, and interactive creations with full 3D preview capabilities.

## ✨ Features

- **Complete Part Library**: Access to all Scrap Mechanic parts including logic gates, sensors, controllers, industrial components, and decorative items
- **Intuitive Connections**: Easy-to-use connection system for 1-to-1, 1-to-many, many-to-1, and many-to-many wiring
- **3D Preview**: Real-time OpenGL-based preview system to visualize your creations
- **Blueprint Management**: Load, save, and manage blueprint files directly from your Scrap Mechanic installation
- **Pre-built Components**: Ready-to-use circuits like RAM, ROM, counters, adders, and more
- **Type Safety**: Full type hints and dataclass-based architecture for better development experience
- **Flexible Positioning**: Support for absolute positioning, rotation, and grid-based layouts

## 🚀 Quick Start

### Installation

```bash
pip install sm_blueprint_lib
```

### Basic Usage

```python
import sm_blueprint_lib as sm
import numpy as np

# Create a new blueprint
bp = sm.Blueprint()

# Add logic gates with different configurations
and_gate = sm.LogicGate(pos=(0, 0, 0), color="ff0000", controller="and")
or_gate = sm.LogicGate(pos=(2, 0, 0), color=sm.PAINT_COLOR.Blue, controller="or")
timer = sm.Timer(pos=(4, 0, 0), color="00ff00", delay=(1, 0))  # 1 second delay

# Connect components
sm.connect(and_gate, or_gate)
sm.connect(or_gate, timer)

# Add to blueprint
bp.add(and_gate, or_gate, timer)

# Save to file
sm.save_blueprint("my_creation", bp)

# Preview in 3D (optional)
sm.preview(bp)
```

## 📚 Documentation

### Core Concepts

#### Blueprint
The main container for your creations:

```python
bp = sm.Blueprint()
# Add parts to the blueprint
bp.add(part1, part2, array_of_parts)
```

#### Positioning
Use the `Pos` class for 3D positioning:

```python
# Multiple ways to specify position
pos1 = sm.Pos(0, 1, 2)
pos2 = (0, 1, 2)  # Tuple automatically converts
pos3 = {"x": 0, "y": 1, "z": 2}  # Dict also works
```

#### Colors
Multiple color formats supported:

```python
# Hex string
color1 = "ff0000"

# RGB tuple
color2 = (255, 0, 0)

# Paint gun colors
color3 = sm.PAINT_COLOR.Red
color4 = sm.PAINT_COLOR.Barberry
```

### Available Parts

#### Logic Components
```python
# Logic gates with different modes
and_gate = sm.LogicGate(pos=(0, 0, 0), controller="and")
or_gate = sm.LogicGate(pos=(1, 0, 0), controller=1)  # 0=and, 1=or, 2=xor, 3=nand, 4=nor, 5=xnor
xor_gate = sm.LogicGate(pos=(2, 0, 0), controller=sm.LogicGateController(mode="xor"))

# Timers and sensors
timer = sm.Timer(pos=(0, 1, 0), delay=(2, 5))  # 2 seconds, 5 ticks
sensor = sm.Sensor(pos=(1, 1, 0))
button = sm.Button(pos=(2, 1, 0))
```

#### Industrial Components
```python
# Engines and wheels
engine = sm.ElectricEngine(pos=(0, 0, 0))
wheel = sm.Wheel(pos=(1, 0, 0))

# Pistons and bearings
piston = sm.Piston(pos=(2, 0, 0))
bearing = sm.Bearing(pos=(3, 0, 0))

# Controllers
controller = sm.Controller(pos=(4, 0, 0))
```

#### Decorative Parts
```python
# Blocks and shapes
block = sm.Block(pos=(0, 0, 0), shape="cube")
pipe = sm.Pipe(pos=(1, 0, 0))
light = sm.Light(pos=(2, 0, 0))
```

### Connection Patterns

#### 1-to-1 Connections
Simple direct connections between two components:

```python
sm.connect(gate1, gate2)
```
![1-to-1 and loop connection](1to1andloop.png)

#### 1-to-Many Connections
Connect one output to multiple inputs (fan-out pattern):

```python
# Connect one output to multiple inputs
sm.connect(source_gate, [gate1, gate2, gate3])
```
![Row to row and 1-to-many connections](rowtorowand1tomany.png)

#### Many-to-1 Connections
Connect multiple outputs to one input (fan-in pattern):

```python
# Connect multiple outputs to one input
sm.connect([gate1, gate2, gate3], target_gate)
```

#### Many-to-Many Connections
Two modes for connecting arrays of components:

```python
# Parallel connection (row-to-row) - each gate connects to corresponding gate
sm.connect(row_a, row_b)  # parallel=True by default

# Cross connection (everything to everything) - each gate connects to all gates
sm.connect(row_a, row_b, parallel=False)
```

![Many-to-1 and many-to-many connections](manytooneandmanytomany.png)

#### Chained Connections
Create loops and chains by chaining connections:

```python
# Chain multiple connections
gate1.connect(gate2).connect(gate3).connect(gate1)  # Creates a loop
```

### Advanced Features

#### 3D Preview
Visualize your creation in real-time:

```python
# Basic preview
sm.preview(bp)

# Custom window size
sm.preview(bp, window_size=(1920, 1080))
```

#### Pre-built Circuits
Use ready-made complex components:

```python
# RAM memory
ram_inputs, ram_outputs = sm.ram(bp, bit_length=8, num_address=16)

# ROM memory  
rom_outputs = sm.rom(bp, page_size=(4, 4), data=[1, 0, 1, 1, 0, 1, 0, 0])

# Counter
counter_outputs, counter_count = sm.counter(bp, bit_length=4)

# Adder
adder_outputs = sm.simple_adder_subtractor(bp, bit_length=8)
```

### MIDI file converter
To convert MIDI files please take a look at `test_midi_converter.py` for more information.

#### Grid Layouts
Create organized layouts using NumPy:

```python
import numpy as np

# Create a 10x10 matrix of logic gates
matrix = np.ndarray((10, 10), dtype=sm.LogicGate)
for x in range(10):
    for z in range(10):
        matrix[x, z] = sm.LogicGate(
            pos=(x, 0, z), 
            color="ffffff", 
            controller="and",
            xaxis=1, zaxis=2  # Custom rotation
        )

bp.add(matrix)
```

#### Blueprint Management
```python
# Load existing blueprint
bp = sm.load_blueprint("path/to/blueprint.json")

# Load from string
bp = sm.load_blueprint_from_blueprint(json_string)

# Export to string
json_data = sm.dump_string_from_blueprint(bp)

# Find blueprints in game folder
blueprint_list = sm.list_blueprints()
my_bp = sm.find_blueprint("My Creation")

# Get blueprint path
bp_path = sm.get_blueprint_path("My Creation")
```

## 🎯 Examples

### Logic Circuit with Multiple Gates

```python
import sm_blueprint_lib as sm

bp = sm.Blueprint()

# Create a simple logic circuit
input_a = sm.Button(pos=(0, 0, 0))
input_b = sm.Button(pos=(0, 0, 2))

# Logic gates
and_gate = sm.LogicGate(pos=(2, 0, 1), controller="and")
or_gate = sm.LogicGate(pos=(4, 0, 1), controller="or")
xor_gate = sm.LogicGate(pos=(6, 0, 1), controller="xor")

# Output indicators
and_light = sm.Light(pos=(2, 1, 1))
or_light = sm.Light(pos=(4, 1, 1))
xor_light = sm.Light(pos=(6, 1, 1))

# Connect everything
sm.connect(input_a, [and_gate, or_gate, xor_gate])
sm.connect(input_b, [and_gate, or_gate, xor_gate])
sm.connect(and_gate, and_light)
sm.connect(or_gate, or_light)
sm.connect(xor_gate, xor_light)

bp.add(input_a, input_b, and_gate, or_gate, xor_gate, and_light, or_light, xor_light)
sm.save_blueprint("logic_demo", bp)
```

### Timed Circuit Loop

```python
# Create a timed loop using timers and logic gates
bp = sm.Blueprint()

loop = [
    sm.Timer(pos=(0, 0, 0), delay=(1, 0)),  # 1 second timer
    sm.LogicGate(pos=(2, 0, 0), controller="not"),
    sm.Light(pos=(4, 0, 0))
]

# Create a loop
loop[0].connect(loop[1]).connect(loop[2]).connect(loop[0])

bp.add(loop)
sm.save_blueprint("timed_loop", bp)
```

## 🛠️ Development

### Building from Source

```bash
git clone https://github.com/MauriceTZ/sm_blueprint_lib.git
cd sm_blueprint_lib
pip install -e .
```

### Dependencies

- **numpy**: Array operations and mathematical functions
- **pygame**: Window management and input handling
- **moderngl**: OpenGL rendering for 3D preview
- **pyglm**: OpenGL mathematics library
- **PyWavefront**: 3D model loading
- ...

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/MauriceTZ/sm_blueprint_lib)
- [PyPI Package](https://pypi.org/project/sm_blueprint_lib/)
- [Issue Tracker](https://github.com/MauriceTZ/sm_blueprint_lib/issues)

## 🎮 Scrap Mechanic

This library is designed to work with **Scrap Mechanic**, a creative sandbox game by Axolot Games. To use the generated blueprints:

1. Install Scrap Mechanic from Steam
2. The library will automatically detect your installation
3. Generated blueprints will appear in your in-game blueprint list

---

*Made with ❤️ by the Scrap Mechanic modding community*