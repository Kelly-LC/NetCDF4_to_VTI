from netCDF4 import Dataset
import numpy as np
from pyevtk.hl import imageToVTK


def netCDF4ToVTK():
    # dstName = /Users/mildred/Desktop/B1850C5X_C35.cam2.h0.0002-05.nc
    dstName = input("Please input the file path:")
    dst = Dataset(dstName, mode='r', format="NETCDF4")
    dict = {}
    myList = []
    i = 1
    for var in dst.variables:
        myList.append(var)
        print("[" + str(i) + "]" + var, end=':\n')
        print("dimensions:" + str(dst.variables[var].dimensions))
        dict[i] = var
        print("------------------")
        i += 1
        for attr in dst[var].ncattrs():
            print('%s: %s' % (attr, dst[var].getncattr(attr)))
        print()

    ind = input("Please input the index to choose one variable:")

    # get the variable name
    index = int(ind)
    index = index - 1
    varString = str(myList[int(index)])

    # varArray = data array
    x, y, z = 1, 1, 1
    varArray = np.array(dst.variables[varString][:], dtype=type(dst.variables))
    varDim = varArray.shape
    print("dimensions:" + str(varDim))
    x = int(varDim[0])
    if (len(varDim) == 2):
        y = int(varDim[1])
    if (len(varDim) == 3):
        y = int(varDim[1])
        z = int(varDim[2])

    # reshape into numpy array
    newArray = np.reshape(varArray.tolist(), (x, y, z), order='C')

    # convert to VTK file
    imageToVTK("./image" + varString, cellData={varString: newArray}, pointData=None)
    print("Conversion is done")

netCDF4ToVTK()