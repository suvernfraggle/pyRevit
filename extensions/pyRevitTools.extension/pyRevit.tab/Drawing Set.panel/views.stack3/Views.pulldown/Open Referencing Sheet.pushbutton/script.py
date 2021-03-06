"""
Copyright (c) 2014-2017 Ehsan Iran-Nejad
Python scripts for Autodesk Revit

This file is part of pyRevit repository at https://github.com/eirannejad/pyRevit

pyRevit is a free set of scripts for Autodesk Revit: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 3, as published by
the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

See this link for a copy of the GNU General Public License protecting this package.
https://github.com/eirannejad/pyRevit/blob/master/LICENSE
"""

__doc__ = 'Opens the sheet containing this view and zooms to the viewport.'

__window__.Close()
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInCategory

uidoc = __revit__.ActiveUIDocument
doc = __revit__.ActiveUIDocument.Document

cl_views = FilteredElementCollector(doc)
shts = cl_views.OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
sheets = sorted(shts, key=lambda x: x.SheetNumber)

curview = doc.ActiveView
count = 0

for s in sheets:
    vpsIds = [doc.GetElement(x).ViewId for x in s.GetAllViewports()]
    if curview.Id in vpsIds:
        uidoc.ActiveView = s
        vpids = s.GetAllViewports()
        for vpid in vpids:
            vp = doc.GetElement(vpid)
            if curview.Id == vp.ViewId:
                ol = vp.GetBoxOutline()
                uidoc.RefreshActiveView()
                avs = uidoc.GetOpenUIViews()
                for uiv in avs:
                    if uiv.ViewId == s.Id:
                        uiv.ZoomAndCenterRectangle(ol.MinimumPoint, ol.MaximumPoint)
