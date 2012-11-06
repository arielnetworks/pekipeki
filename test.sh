#!/bin/sh

bin/nose
bin/pyflakes pekipeki
bin/pep8 --repeat --ignore E303,W391,E501 pekipeki
