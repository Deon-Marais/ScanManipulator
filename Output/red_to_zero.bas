Attribute VB_Name = "Module1"
Sub Make_red_zeros()
Attribute Make_red_zeros.VB_ProcData.VB_Invoke_Func = " \n14"
'
' Make_red_zeros Macro
'

'
    Dim x As Integer
    numcols = Range("A2", Range("A2").End(xlToRight)).Columns.Count
    Dim y As Integer
    numrows = Range("A2", Range("A2").End(xlDown)).Rows.Count
    Range("A2").Select
    For x = 1 To numcols
        For y = 1 To numrows
            If ActiveCell.Font.ColorIndex = 3 Then
                ActiveCell.Value = 0
            End If
            ActiveCell.Offset(1, 0).Select
        Next
        Range("A2").Select
        ActiveCell.Offset(0, x).Select
    Next
End Sub
