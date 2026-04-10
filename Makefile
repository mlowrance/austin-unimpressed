# Open Watcom C/C++ x86 16-bit Makefile
# Targets: DOS Real Mode

CC = wcl
CFLAGS = -bt=dos -0 -ms -zq -i=include
LDFLAGS = 
OBJ_DIR = bin
SRC_DIR = src
TARGET = $(OBJ_DIR)/AUSTIN.EXE

# Source files
SRCS = $(wildcard $(SRC_DIR)/*.c)

.PHONY: all build run clean sd-card ftp hardware

all: build

build: $(TARGET)

$(TARGET): $(SRCS)
	@mkdir -p $(OBJ_DIR)
	$(CC) $(CFLAGS) -fe=$(TARGET) $(SRCS)

run: build
	dosbox-x -c "mount c $(CURDIR)/bin" -c "c:" -c "AUSTIN.EXE" -c "exit"

# Stub targets for future needs
hardware:
	@echo "Building for hardware (currently same as build)..."
	$(MAKE) build

sd-card: build
	@echo "TODO: Copy $(TARGET) to SD card..."
	# cp $(TARGET) /Volumes/SD_CARD/

ftp: build
	@echo "TODO: Push $(TARGET) via FTP..."
	# curl -T $(TARGET) ftp://dos-machine/

clean:
	rm -rf $(OBJ_DIR)/*.EXE $(OBJ_DIR)/*.obj $(OBJ_DIR)/*.map
