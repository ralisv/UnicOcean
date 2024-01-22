Here's the class hierarchy that is used in this project. (Work in progress)
```mermaid
classDiagram
    OceanObject <|-- MovingObject
    OceanObject <|-- StaticObject
    MovingObject <|-- Fish

    class OceanObject {
      skin
      zIndex
      anchorCoordinates
      update()
      on_collision()
    }
    class StaticObject {
    }
    class MovingObject {
      direction
      move()
    }
    class Fish {
      isCarnivorous
      mouthCoordinates
    }
```

# OceanObject
Base for all other classes.
# MovingObject
For objects that can move.
# StaticObject
Objects that don't move.
# Fish
Fishes