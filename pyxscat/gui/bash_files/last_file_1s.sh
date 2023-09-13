#!/bin/sh
find $1 -name "$2" -newermt "-1 seconds"