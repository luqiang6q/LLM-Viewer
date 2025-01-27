import numpy as np

def numpy_value_to_python(d):
    if isinstance(d, dict):
        for key in d:
            if isinstance(d[key],np.ndarray):
                d[key]=d[key].tolist()
            if isinstance(d[key],np.int64):
                d[key]=int(d[key])
            if isinstance(d[key],np.int32):
                d[key]=int(d[key])
            if isinstance(d[key],np.float32):
                d[key]=float(d[key])
            if isinstance(d[key],np.float64):
                d[key]=float(d[key])
    elif isinstance(d,np.ndarray):
        d=d.tolist()
    elif isinstance(d,np.int64):
        d=int(d)
    elif isinstance(d,np.int32):
        d=int(d)
    elif isinstance(d,np.float32):
        d=float(d)
    elif isinstance(d,np.float64):
        d=float(d)
    return d

def str_number_1024(num):
    if num > (1<<40):
        return f"{num/(1<<40):.1f}T"
    elif num > (1<<30):
        return f"{num/(1<<30):.1f}G"
    elif num > (1<<20):
        return f"{num/(1<<20):.1f}M"
    elif num > (1<<10):
        return f"{num/(1<<10):.1f}K"
    else:
        return f"{num:.1f}"
    

def str_number(num):
    if num > 1e14:
        return f"{num/1e12:.0f}T"
    elif num > 1e12:
        return f"{num/1e12:.1f}T"
    elif num>1e11:
        return f"{num/1e9:.0f}G"
    elif num > 1e9:
        return f"{num/1e9:.1f}G"
    elif num > 1e8:
        return f"{num/1e6:.0f}M"
    elif num > 1e6:
        return f"{num/1e6:.1f}M"
    elif num > 1e5:
        return f"{num/1e3:.0f}K"
    elif num > 1e3:
        return f"{num/1e3:.1f}K"
    elif num >= 1:
        return f"{num:.1f}"
    else:
        return f"{num:.2f}"

def str_number_time(num):
    if num >= 1:
        return f"{num:.1f}"
    elif num > 1e-3:
        return f"{num*1e3:.1f}m"
    elif num > 1e-6:
        return f"{num*1e6:.1f}u"
    elif num > 1e-9:
        return f"{num*1e9:.1f}n"
    else:
        return f"{num:.0f}"