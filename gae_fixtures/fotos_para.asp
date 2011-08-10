<%@ CodePage=65001 Language="VBScript"%>
<%
On Error Resume Next
Response.Charset="UTF-8"
Response.CodePage = 65001

Set objFSO = CreateObject("Scripting.FileSystemObject")
objStartFolder = Server.MapPath("fotos/" + request("id"))

Set objFolder = objFSO.GetFolder(objStartFolder)

Set colFiles = objFolder.Files
For Each objFile in colFiles
    Response.Write( objFile.Name + vbLf )
Next

%>