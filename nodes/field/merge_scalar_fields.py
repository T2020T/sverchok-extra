
import numpy as np

import bpy
from bpy.props import FloatProperty, EnumProperty, BoolProperty, IntProperty, StringProperty

from sverchok.node_tree import SverchCustomTreeNode, throttled
from sverchok.data_structure import updateNode, zip_long_repeat, fullList, match_long_repeat, ensure_nesting_level
from sverchok.utils.logging import info, exception

from sverchok_extra.data import SvExMergedScalarField, SvExScalarField

class SvExMergeScalarFieldsNode(bpy.types.Node, SverchCustomTreeNode):
    """
    Triggers: Merge / Join Scalar Fields
    Tooltip: Merge a list of scalar fields into one
    """
    bl_idname = 'SvExMergeScalarFieldsNode'
    bl_label = 'Join Scalar Fields'
    bl_icon = 'OUTLINER_OB_EMPTY'
    sv_icon = 'SV_VORONOI'

    modes = [
        ('MIN', "Minimum", "Minimal value of all fields", 0),
        ('MAX', "Maximum", "Maximal value of all fields", 1),
        ('AVG', "Average", "Average value of all fields", 2),
        ('SUM', "Sum", "Sum value of all fields", 3),
    ]

    mode : EnumProperty(
        name = "Mode",
        items = modes,
        default = 'AVG',
        update = updateNode)

    def sv_init(self, context):
        self.inputs.new('SvExScalarFieldSocket', "Fields").display_shape = 'CIRCLE_DOT'
        self.outputs.new('SvExScalarFieldSocket', "Field").display_shape = 'CIRCLE_DOT'

    def draw_buttons(self, context, layout):
        layout.prop(self, "mode", text="")

    def process(self):
        if not any(socket.is_linked for socket in self.outputs):
            return

        fields_s = self.inputs['Fields'].sv_get()
        if isinstance(fields_s[0], SvExScalarField):
            fields_s = [fields_s]

        fields_out = []
        for fields in fields_s:
            field = SvExMergedScalarField(self.mode, fields)
            fields_out.append(field)
        self.outputs['Field'].sv_set(fields_out)

def register():
    bpy.utils.register_class(SvExMergeScalarFieldsNode)

def unregister():
    bpy.utils.unregister_class(SvExMergeScalarFieldsNode)
