#!/usr/bin/env bash

BASEDIR=$(dirname "$0")
mkdir -p "$BASEDIR/../collections/ansible_collections/pureport"
(cd  "$BASEDIR/../collections/ansible_collections/pureport" && ln -s ../../../../.. fabric)

