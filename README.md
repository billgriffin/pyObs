# pyObs
Python Observation Coding System

You must install python 2.7, numpy, and wxPython. Python comes installed on Linux operating systems.  For OS X or Windows, complete free distributions are available at:

https://www.python.org/

https://www.anaconda.com/download/

https://www.enthought.com/product/canopy/

Depending on installation, you may have to install wxPython separately.  It is located at www.wxpython.org


Note that when using conda (from Anaconda) on MacOS X, the following instructions can be used to test pyObs:
_____________________________________
conda create --name pyObs python=2.7

source activate pyObs

conda install wxPython

conda install numpy

pythonw pyObs_Ind.py
_____________________________________

To run pyObs, go to the directory housing pyObs and at the prompt type:

$ python pyObs_Ind.py

The Variants and the ASD Illustration are invoked in a similar manner:

$ python VisualAttention.py

$ python AffectExpress.py

$ python ASDVisualReference.py

Make sure that you are in the directory housing the desired python module. 

PyObs has not be converted to work with Python 3.4+ and wxPython Phoenix.  Contact me if you have difficulty getting the modules to work: william.griffin@asu.edu
