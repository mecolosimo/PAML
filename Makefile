OBJS = src/paml/uint256/uint256.o

# Target library name
TARGET = src/paml/libmath.dylib

ifdef DEBUG
DEBUGFLGS = -g
else
DEBUGFLGS =
endif

ASFLAGS = -arch arm64 $(DEBUGFLGS)

# Link the object file into a dynamic library
$(TARGET): $(OBJS)
	clang -dynamiclib -o $(TARGET) $(OBJS)

%.o: %.s
	as $(ASFLAGS) $< -o $@

.PHONY: clean all
all: $(TARGET)

# Cleanup
clean:
	rm -rf $(OBJS) $(TARGET)