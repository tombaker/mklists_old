"""According to Martelli, the simplest way to share objects 
(such as functions and constants) among modules in package P:
    
Group shared objects in file P/Common.py.

Then:
    -- `import Common` 
       from every module in package that needs to access the objects
       -- refer to Common.f, Common.K...
"""
