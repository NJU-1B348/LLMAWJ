class InferTag:
    # vanilla tags
    class DefectType:
        NPE ="npe"
        DF = "doubleFree"
        RL = "resourceLeak"
        AOB = "array_index_out_bounds"

    TYPE = "type"
    LOC = "locations"
    
    class LocTag:
        TYPE = "type"
        SRC = "source"
        SINK = "sink"
        V = "var"
        F = "file"
        L = "line"
        C = "column"


class IWFTag:
    # vanilla tags
    class DefectType:
        NPE = "Null Pointer Error"
        RL = "Resource Leak"
        AOB = "Array Index Out Bounds"
        NF = "Never Free"
        DF = "Double Free"
        UAF = "Use After Free"
        PL = "Partial Leak"

    DT = "DefectType"
    LOC = "Location"
    l = "ln"
    c = "cl"
    f = "fl"
    Func = "Function"
    Des = "Description"
    CFP = "ConditionalFreePath"
    BL = "BranchLoc"
    BC = "BranchCond"
    true = "True"
    false = "False"
    E = "Events"
    # new tags
    Code = "CodeNear"
    Flag = "SuccessTransform"
    Msg = "TransformMessage"
    V = "Var"


class TransformMessage:
    AC = ""
    DFF = "Duplicated Files Found"
    NSF = "No Such File"
    CIV = "Cannot Infer VarName"
    DFFIC = "Duplicated Files Found In Conditions Analysis"
    NSFIC = "No Such File In Conditions Analysis"
    
InferTag_to_IWFTag_dict = {
    InferTag.DefectType.NPE:    IWFTag.DefectType.NPE,
    InferTag.DefectType.AOB:    IWFTag.DefectType.AOB,
    InferTag.DefectType.DF:     IWFTag.DefectType.DF,
    InferTag.DefectType.RL:     IWFTag.DefectType.RL,
}