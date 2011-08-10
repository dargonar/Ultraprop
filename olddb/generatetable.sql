-- DBWScript v3.3
-- Database: C:\WDIR\related\ultrageo\Copia de dbcontents.mdb

CREATE TABLE [~TMPCLP152941] (

);
CREATE TABLE [MSysCompactError] (
	[ErrorCode] LONG,
	[ErrorDescription] MEMO WITH COMPRESSION,
	[ErrorRecid] BINARY,
	[ErrorTable] TEXT(255) WITH COMPRESSION
);
ALTER TABLE [MSysCompactError] ALLOW ZERO LENGTH [ErrorDescription];
ALTER TABLE [MSysCompactError] ALLOW ZERO LENGTH [ErrorTable];
CREATE TABLE [tbl_administrador] (
	[password] TEXT(50) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([password])
);
ALTER TABLE [tbl_administrador] DENY ZERO LENGTH [password];
CREATE TABLE [tbl_Fotos] (
	[Id] AUTOINCREMENT,
	[PROP_Id] LONG DEFAULT 0,
	[Titulo] TEXT(100) WITH COMPRESSION DEFAULT "Sin titulo",
	[Tituloimagen] TEXT(100) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([Id])
);
ALTER TABLE [tbl_Fotos] DENY ZERO LENGTH [Titulo];
ALTER TABLE [tbl_Fotos] DENY ZERO LENGTH [Tituloimagen];
CREATE TABLE [tbl_LOGS_Submit] (
	[CTLOG_Id] AUTOINCREMENT,
	[CTLOG_OperID] LONG DEFAULT 0,
	[CTLOG_InmID] LONG DEFAULT 0,
	[CTLOG_Date] DATETIME,
	[CTLOG_FName] TEXT(255) WITH COMPRESSION,
	[CTLOG_LName] TEXT(255) WITH COMPRESSION,
	[CTLOG_Address] TEXT(255) WITH COMPRESSION,
	[CTLOG_City] TEXT(255) WITH COMPRESSION,
	[CTLOG_Province] TEXT(255) WITH COMPRESSION,
	[CTLOG_Country] TEXT(255) WITH COMPRESSION,
	[CTLOG_Phone] TEXT(255) WITH COMPRESSION,
	[CTLOG_ClientEmail] TEXT(255) WITH COMPRESSION,
	[CTLOG_InmEmailFail] BIT NOT NULL,
	[CTLOG_InmEmail] TEXT(255) WITH COMPRESSION,
	[CTLOG_Comments] MEMO WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([CTLOG_Id])
);
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_FName];
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_LName];
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_Address];
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_City];
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_Province];
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_Country];
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_Phone];
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_ClientEmail];
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_InmEmail];
ALTER TABLE [tbl_LOGS_Submit] ALLOW ZERO LENGTH [CTLOG_Comments];
ALTER TABLE [tbl_LOGS_Submit] FORMAT [CTLOG_InmEmailFail] SET "Yes/No";
CREATE TABLE [tbl_OperacionesPosibles] (
	[OP_Id] AUTOINCREMENT,
	[OP_PROP_Id] LONG DEFAULT 0,
	[OP_OPER_Id] TEXT(2) WITH COMPRESSION,
	[OP_MONEDAS_Id] TEXT(2) WITH COMPRESSION,
	[OP_Monto] LONG DEFAULT 0,
	[OP_Expensas] TEXT(50) WITH COMPRESSION,
	[OP_Financiacion] BIT NOT NULL,
	[OP_Financiacion_detalle] MEMO WITH COMPRESSION,
	[OP_Destacada] BIT NOT NULL,
	[OP_DestaWebclient] BIT NOT NULL,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([OP_Id])
);
ALTER TABLE [tbl_OperacionesPosibles] DENY ZERO LENGTH [OP_OPER_Id];
ALTER TABLE [tbl_OperacionesPosibles] DENY ZERO LENGTH [OP_MONEDAS_Id];
ALTER TABLE [tbl_OperacionesPosibles] ALLOW ZERO LENGTH [OP_Expensas];
ALTER TABLE [tbl_OperacionesPosibles] ALLOW ZERO LENGTH [OP_Financiacion_detalle];
ALTER TABLE [tbl_OperacionesPosibles] FORMAT [OP_Financiacion] SET "Yes/No";
ALTER TABLE [tbl_OperacionesPosibles] FORMAT [OP_Destacada] SET "Yes/No";
ALTER TABLE [tbl_OperacionesPosibles] FORMAT [OP_DestaWebclient] SET "Yes/No";
CREATE TABLE [tbl_PARAM_Anunciantes] (
	[AD_ID] AUTOINCREMENT,
	[AD_Name] TEXT(50) WITH COMPRESSION,
	[AD_FileName] TEXT(50) WITH COMPRESSION,
	[AD_Link] TEXT(255) WITH COMPRESSION,
	[AD_LinkTarget] TEXT(50) WITH COMPRESSION,
	[AD_IsFlash] BIT NOT NULL,
	[AD_InternalLink] BIT NOT NULL,
	[AD_OrderTypeRnd] BIT NOT NULL,
	[AD_Order] LONG DEFAULT 0,
	[AD_Height] LONG DEFAULT 0,
	[AD_Width] LONG DEFAULT 0,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([AD_ID])
);
ALTER TABLE [tbl_PARAM_Anunciantes] ALLOW ZERO LENGTH [AD_Name];
ALTER TABLE [tbl_PARAM_Anunciantes] ALLOW ZERO LENGTH [AD_FileName];
ALTER TABLE [tbl_PARAM_Anunciantes] ALLOW ZERO LENGTH [AD_Link];
ALTER TABLE [tbl_PARAM_Anunciantes] ALLOW ZERO LENGTH [AD_LinkTarget];
ALTER TABLE [tbl_PARAM_Anunciantes] FORMAT [AD_IsFlash] SET "Yes/No";
ALTER TABLE [tbl_PARAM_Anunciantes] FORMAT [AD_InternalLink] SET "Yes/No";
ALTER TABLE [tbl_PARAM_Anunciantes] FORMAT [AD_OrderTypeRnd] SET "Yes/No";
CREATE TABLE [tbl_PARAM_Inmobiliarias] (
	[INM_Id] AUTOINCREMENT,
	[INM_Nombre] TEXT(50) WITH COMPRESSION,
	[INM_Direccion] TEXT(100) WITH COMPRESSION,
	[INM_Telefono] TEXT(40) WITH COMPRESSION,
	[INM_Fax] TEXT(20) WITH COMPRESSION,
	[INM_Email] TEXT(50) WITH COMPRESSION,
	[INM_Url] TEXT(50) WITH COMPRESSION,
	[INM_Pass] TEXT(10) WITH COMPRESSION,
	[INM_Destacados] LONG DEFAULT 0,
	[INM_Desabilitada] BIT NOT NULL,
	[INM_Color] TEXT(50) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([INM_Id])
);
ALTER TABLE [tbl_PARAM_Inmobiliarias] ALLOW ZERO LENGTH [INM_Nombre];
ALTER TABLE [tbl_PARAM_Inmobiliarias] ALLOW ZERO LENGTH [INM_Direccion];
ALTER TABLE [tbl_PARAM_Inmobiliarias] ALLOW ZERO LENGTH [INM_Telefono];
ALTER TABLE [tbl_PARAM_Inmobiliarias] ALLOW ZERO LENGTH [INM_Fax];
ALTER TABLE [tbl_PARAM_Inmobiliarias] ALLOW ZERO LENGTH [INM_Email];
ALTER TABLE [tbl_PARAM_Inmobiliarias] ALLOW ZERO LENGTH [INM_Url];
ALTER TABLE [tbl_PARAM_Inmobiliarias] DENY ZERO LENGTH [INM_Pass];
ALTER TABLE [tbl_PARAM_Inmobiliarias] ALLOW ZERO LENGTH [INM_Color];
ALTER TABLE [tbl_PARAM_Inmobiliarias] FORMAT [INM_Desabilitada] SET "Yes/No";
CREATE TABLE [tbl_PARAM_Localidades] (
	[LOCAL_PROV_Id] DOUBLE,
	[LOCAL_Id] DOUBLE,
	[LOCAL_Nombre] TEXT(255) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([LOCAL_PROV_Id], [LOCAL_Id])
);
ALTER TABLE [tbl_PARAM_Localidades] DENY ZERO LENGTH [LOCAL_Nombre];
CREATE TABLE [tbl_PARAM_Lugar] (
	[LUGAR_Id] TEXT(1) WITH COMPRESSION,
	[LUGAR_Descripcion] TEXT(30) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([LUGAR_Id])
);
ALTER TABLE [tbl_PARAM_Lugar] DENY ZERO LENGTH [LUGAR_Id];
ALTER TABLE [tbl_PARAM_Lugar] DENY ZERO LENGTH [LUGAR_Descripcion];
CREATE TABLE [tbl_PARAM_Monedas] (
	[MONEDAS_Id] TEXT(2) WITH COMPRESSION,
	[MONEDAS_Descripcion] TEXT(50) WITH COMPRESSION,
	[MONEDAS_Signo] TEXT(5) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([MONEDAS_Id])
);
ALTER TABLE [tbl_PARAM_Monedas] DENY ZERO LENGTH [MONEDAS_Id];
ALTER TABLE [tbl_PARAM_Monedas] DENY ZERO LENGTH [MONEDAS_Descripcion];
ALTER TABLE [tbl_PARAM_Monedas] DENY ZERO LENGTH [MONEDAS_Signo];
CREATE TABLE [tbl_PARAM_Partidos] (
	[PART_PROV_Id] DOUBLE,
	[PART_LOCAL_Id] DOUBLE,
	[PART_Id] DOUBLE,
	[PART_Nombre] TEXT(255) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([PART_PROV_Id], [PART_LOCAL_Id], [PART_Id])
);
ALTER TABLE [tbl_PARAM_Partidos] DENY ZERO LENGTH [PART_Nombre];
CREATE TABLE [tbl_PARAM_Provincias] (
	[PROV_Id] SMALLINT DEFAULT 0,
	[PROV_Nombre] TEXT(50) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([PROV_Id])
);
ALTER TABLE [tbl_PARAM_Provincias] DENY ZERO LENGTH [PROV_Nombre];
CREATE TABLE [tbl_PARAM_TiposOperacion] (
	[OPER_Id] TEXT(2) WITH COMPRESSION,
	[OPER_Descripcion] TEXT(50) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([OPER_Id])
);
ALTER TABLE [tbl_PARAM_TiposOperacion] DENY ZERO LENGTH [OPER_Id];
ALTER TABLE [tbl_PARAM_TiposOperacion] DENY ZERO LENGTH [OPER_Descripcion];
CREATE TABLE [tbl_PARAM_TiposPropiedad] (
	[TIPROP_Id] TEXT(2) WITH COMPRESSION,
	[TIPROP_Descripcion] TEXT(50) WITH COMPRESSION,
	[imagenboton] TEXT(50) WITH COMPRESSION,
	[imagenbotonv] TEXT(50) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([TIPROP_Id])
);
ALTER TABLE [tbl_PARAM_TiposPropiedad] DENY ZERO LENGTH [TIPROP_Id];
ALTER TABLE [tbl_PARAM_TiposPropiedad] DENY ZERO LENGTH [TIPROP_Descripcion];
ALTER TABLE [tbl_PARAM_TiposPropiedad] DENY ZERO LENGTH [imagenboton];
ALTER TABLE [tbl_PARAM_TiposPropiedad] DENY ZERO LENGTH [imagenbotonv];
CREATE TABLE [tbl_Planos] (
	[Id] AUTOINCREMENT,
	[PROP_Id] LONG DEFAULT 0,
	[Titulo] MEMO WITH COMPRESSION,
	[Tituloimagen] TEXT(50) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([Id])
);
ALTER TABLE [tbl_Planos] DENY ZERO LENGTH [Titulo];
ALTER TABLE [tbl_Planos] DENY ZERO LENGTH [Tituloimagen];
CREATE TABLE [tbl_Propiedades] (
	[PROP_Id] AUTOINCREMENT,
	[PROP_FechaIngreso] DATETIME,
	[PROP_Inmobiliaria] LONG DEFAULT 0,
	[PROP_TIPROP_Id] TEXT(2) WITH COMPRESSION,
	[PROP_PROV_Id] SMALLINT DEFAULT 0,
	[PROP_LOCAL_Id] SMALLINT DEFAULT 0,
	[PROP_PART_Id] SMALLINT DEFAULT 0,
	[PROP_Lugar] TEXT(1) WITH COMPRESSION,
	[PROP_barrio] TEXT(50) WITH COMPRESSION,
	[PROP_Calle] TEXT(50) WITH COMPRESSION,
	[PROP_Nro] TEXT(10) WITH COMPRESSION,
	[PROP_PisoDpto] TEXT(30) WITH COMPRESSION,
	[PROP_DireccionOtros] MEMO WITH COMPRESSION,
	[PROP_ServAgua] BIT NOT NULL,
	[PROP_ServLuz] BIT NOT NULL,
	[PROP_ServGasNatural] BIT NOT NULL,
	[PROP_ServGasGarrafa] BIT NOT NULL,
	[PROP_ServCloacas] BIT NOT NULL,
	[PROP_ServCable] BIT NOT NULL,
	[PROP_ServTelefono] BIT NOT NULL,
	[PROP_SupLibre] TEXT(25) WITH COMPRESSION,
	[PROP_SupCubierta] TEXT(25) WITH COMPRESSION,
	[PROP_SupTotal] TEXT(25) WITH COMPRESSION,
	[PROP_Dormitorios] TINYINT DEFAULT 0,
	[PROP_Plantas] TINYINT DEFAULT 0,
	[PROP_Ambientes] TINYINT DEFAULT 0,
	[PROP_Antiguedad] SMALLINT DEFAULT 0,
	[PROP_Banos] TINYINT DEFAULT 0,
	[PROP_Edificacion] TEXT(1) WITH COMPRESSION,
	[PROP_Amoblado] BIT NOT NULL,
	[PROP_Cochera] BIT NOT NULL,
	[PROP_Dependencia] BIT NOT NULL,
	[PROP_Parque] BIT NOT NULL,
	[PROP_VMF] BIT NOT NULL,
	[PROP_Patio] BIT NOT NULL,
	[PROP_Pileta] BIT NOT NULL,
	[PROP_Asfalto] BIT NOT NULL,
	[PROP_Terraza] BIT NOT NULL,
	[PROP_DescripcionGeneral] MEMO WITH COMPRESSION,
	[PROP_360] TEXT(50) WITH COMPRESSION,
	[PPROP_Mapa] TEXT(50) WITH COMPRESSION,
	[PROP_Vendido] BIT NOT NULL,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([PROP_Id])
);
ALTER TABLE [tbl_Propiedades] DENY ZERO LENGTH [PROP_TIPROP_Id];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_Lugar];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_barrio];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_Calle];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_Nro];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_PisoDpto];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_DireccionOtros];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_SupLibre];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_SupCubierta];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_SupTotal];
ALTER TABLE [tbl_Propiedades] DENY ZERO LENGTH [PROP_Edificacion];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_DescripcionGeneral];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PROP_360];
ALTER TABLE [tbl_Propiedades] ALLOW ZERO LENGTH [PPROP_Mapa];
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_FechaIngreso] SET "Short Date";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_ServAgua] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_ServLuz] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_ServGasNatural] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_ServGasGarrafa] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_ServCloacas] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_ServCable] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_ServTelefono] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_Amoblado] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_Cochera] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_Dependencia] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_Parque] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_VMF] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_Patio] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_Pileta] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_Asfalto] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_Terraza] SET "Yes/No";
ALTER TABLE [tbl_Propiedades] FORMAT [PROP_Vendido] SET "Yes/No";
CREATE TABLE [tbl_Usuarios] (
	[Id] AUTOINCREMENT,
	[Contrasena] TEXT(32) WITH COMPRESSION NOT NULL,
	[Nombre] TEXT(50) WITH COMPRESSION,
	[Apellido] TEXT(50) WITH COMPRESSION,
	[Direccion] TEXT(50) WITH COMPRESSION,
	[Numero] TEXT(10) WITH COMPRESSION,
	[Piso] TEXT(3) WITH COMPRESSION,
	[Dpto] TEXT(3) WITH COMPRESSION,
	[Localidad] TEXT(50) WITH COMPRESSION,
	[Provincia] TEXT(50) WITH COMPRESSION,
	[Provincia1] TEXT(50) WITH COMPRESSION,
	[Pais] TEXT(50) WITH COMPRESSION,
	[Tel] TEXT(30) WITH COMPRESSION,
	[email] TEXT(50) WITH COMPRESSION,
	[Edad] TEXT(10) WITH COMPRESSION,
	[EstadoCivil] TEXT(15) WITH COMPRESSION,
	[Sexo] TEXT(3) WITH COMPRESSION,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([Id])
);
ALTER TABLE [tbl_Usuarios] DENY ZERO LENGTH [Contrasena];
ALTER TABLE [tbl_Usuarios] DENY ZERO LENGTH [Nombre];
ALTER TABLE [tbl_Usuarios] DENY ZERO LENGTH [Apellido];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Direccion];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Numero];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Piso];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Dpto];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Localidad];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Provincia];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Provincia1];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Pais];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Tel];
ALTER TABLE [tbl_Usuarios] DENY ZERO LENGTH [email];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Edad];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [EstadoCivil];
ALTER TABLE [tbl_Usuarios] ALLOW ZERO LENGTH [Sexo];
CREATE TABLE [tbl_Usuarios_Propiedades] (
	[Id] AUTOINCREMENT,
	[Contrasena] TEXT(50) WITH COMPRESSION,
	[Usuario] TEXT(50) WITH COMPRESSION,
	[OP_Id] LONG DEFAULT 0,
	CONSTRAINT [PrimaryKey] PRIMARY KEY ([Id])
);
ALTER TABLE [tbl_Usuarios_Propiedades] DENY ZERO LENGTH [Contrasena];
ALTER TABLE [tbl_Usuarios_Propiedades] DENY ZERO LENGTH [Usuario];
CREATE INDEX [Id]
	ON [tbl_administrador] ([password]);
CREATE INDEX [PROP_Id]
	ON [tbl_Fotos] ([PROP_Id]);
CREATE INDEX [CTLOG_Id]
	ON [tbl_LOGS_Submit] ([CTLOG_Id]);
CREATE INDEX [CTLOG_InmID]
	ON [tbl_LOGS_Submit] ([CTLOG_InmID]);
CREATE INDEX [CTLOG_OperID]
	ON [tbl_LOGS_Submit] ([CTLOG_OperID]);
CREATE INDEX [OP_OPER_Id]
	ON [tbl_OperacionesPosibles] ([OP_OPER_Id]);
CREATE INDEX [OP_PROP_Id]
	ON [tbl_OperacionesPosibles] ([OP_PROP_Id]);
CREATE INDEX [AD_ID]
	ON [tbl_PARAM_Anunciantes] ([AD_ID]);
CREATE INDEX [PROP_Id]
	ON [tbl_PARAM_Inmobiliarias] ([INM_Id]);
CREATE INDEX [LUGAR_Id]
	ON [tbl_PARAM_Lugar] ([LUGAR_Id]);
CREATE INDEX [MONEDAS_Id]
	ON [tbl_PARAM_Monedas] ([MONEDAS_Id]);
CREATE INDEX [PART_Id]
	ON [tbl_PARAM_Partidos] ([PART_Id]);
CREATE INDEX [PART_LOCAL_Id]
	ON [tbl_PARAM_Partidos] ([PART_LOCAL_Id]);
CREATE INDEX [PART_PROV_Id]
	ON [tbl_PARAM_Partidos] ([PART_PROV_Id]);
CREATE INDEX [PROV_Id]
	ON [tbl_PARAM_Provincias] ([PROV_Id]);
CREATE INDEX [OPER_Id]
	ON [tbl_PARAM_TiposOperacion] ([OPER_Id]);
CREATE INDEX [PARAM_Id]
	ON [tbl_PARAM_TiposPropiedad] ([TIPROP_Id]);
CREATE INDEX [PROP_Id]
	ON [tbl_Planos] ([PROP_Id]);
CREATE INDEX [PROP_Id]
	ON [tbl_Propiedades] ([PROP_Id]);
CREATE INDEX [PROP_OPER_Id]
	ON [tbl_Propiedades] ([PROP_TIPROP_Id]);
CREATE INDEX [Id]
	ON [tbl_Usuarios] ([Id]);
CREATE INDEX [Id]
	ON [tbl_Usuarios_Propiedades] ([Id]);
CREATE INDEX [Propiedad_Id]
	ON [tbl_Usuarios_Propiedades] ([OP_Id]);
CREATE INDEX [email]
	ON [tbl_Usuarios_Propiedades] ([Usuario]);
ALTER TABLE [tbl_Fotos]
	ADD CONSTRAINT [tbl_Propiedadestbl_Fotos]
	FOREIGN KEY ([PROP_Id]) REFERENCES
		[tbl_Propiedades] ([PROP_Id])
	ON UPDATE CASCADE
	ON DELETE CASCADE;
ALTER TABLE [tbl_OperacionesPosibles]
	ADD CONSTRAINT [tbl_PARAM_Monedastbl_OperacionesPosibles]
	FOREIGN KEY ([OP_MONEDAS_Id]) REFERENCES
		[tbl_PARAM_Monedas] ([MONEDAS_Id])
	ON UPDATE CASCADE;
ALTER TABLE [tbl_OperacionesPosibles]
	ADD CONSTRAINT [tbl_PARAM_TiposOperaciontbl_OperacionesPosibles]
	FOREIGN KEY ([OP_OPER_Id]) REFERENCES
		[tbl_PARAM_TiposOperacion] ([OPER_Id])
	ON UPDATE CASCADE;
ALTER TABLE [tbl_OperacionesPosibles]
	ADD CONSTRAINT [tbl_Propiedadestbl_OperacionesPosibles]
	FOREIGN KEY ([OP_PROP_Id]) REFERENCES
		[tbl_Propiedades] ([PROP_Id])
	ON UPDATE CASCADE
	ON DELETE CASCADE;
ALTER TABLE [tbl_PARAM_Localidades]
	ADD CONSTRAINT [tbl_Propiedadestbl_PARAM_Localidades]
	FOREIGN KEY NO INDEX ([LOCAL_PROV_Id], [LOCAL_Id]) REFERENCES
		[tbl_Propiedades] ([PROP_PROV_Id], [PROP_LOCAL_Id]);
ALTER TABLE [tbl_PARAM_Partidos]
	ADD CONSTRAINT [tbl_Propiedadestbl_PARAM_Partidos]
	FOREIGN KEY NO INDEX ([PART_PROV_Id], [PART_LOCAL_Id], [PART_Id]) REFERENCES
		[tbl_Propiedades] ([PROP_PROV_Id], [PROP_LOCAL_Id], [PROP_PART_Id]);
ALTER TABLE [tbl_Planos]
	ADD CONSTRAINT [tbl_Propiedadestbl_Planos]
	FOREIGN KEY ([PROP_Id]) REFERENCES
		[tbl_Propiedades] ([PROP_Id])
	ON UPDATE CASCADE
	ON DELETE CASCADE;
ALTER TABLE [tbl_Propiedades]
	ADD CONSTRAINT [tbl_PARAM_Inmobiliariastbl_Propiedades]
	FOREIGN KEY ([PROP_Inmobiliaria]) REFERENCES
		[tbl_PARAM_Inmobiliarias] ([INM_Id])
	ON UPDATE CASCADE
	ON DELETE CASCADE;
ALTER TABLE [tbl_Propiedades]
	ADD CONSTRAINT [tbl_PARAM_Lugartbl_Propiedades]
	FOREIGN KEY ([PROP_Lugar]) REFERENCES
		[tbl_PARAM_Lugar] ([LUGAR_Id])
	ON UPDATE CASCADE;
ALTER TABLE [tbl_Propiedades]
	ADD CONSTRAINT [tbl_PARAM_Provinciastbl_Propiedades]
	FOREIGN KEY NO INDEX ([PROP_PROV_Id]) REFERENCES
		[tbl_PARAM_Provincias] ([PROV_Id]);
ALTER TABLE [tbl_Propiedades]
	ADD CONSTRAINT [tbl_PARAM_TiposPropiedadtbl_Propiedades]
	FOREIGN KEY ([PROP_TIPROP_Id]) REFERENCES
		[tbl_PARAM_TiposPropiedad] ([TIPROP_Id])
	ON UPDATE CASCADE;
ALTER TABLE [tbl_Usuarios_Propiedades]
	ADD CONSTRAINT [tbl_OperacionesPosiblestbl_Usuarios_Propiedades]
	FOREIGN KEY ([OP_Id]) REFERENCES
		[tbl_OperacionesPosibles] ([OP_Id])
	ON UPDATE CASCADE
	ON DELETE CASCADE;
CREATE VIEW [Cons_Destacada] AS SELECT [tbl_Propiedades].[PROP_Id], [tbl_PARAM_Localidades].[LOCAL_Nombre], [tbl_OperacionesPosibles].[OP_Destacada], [tbl_Propiedades].[PROP_SupTotal], [tbl_OperacionesPosibles].[OP_Monto], [tbl_OperacionesPosibles].[OP_Id], [tbl_PARAM_Monedas].[MONEDAS_Signo], [tbl_PARAM_TiposOperacion].[OPER_Descripcion], [tbl_PARAM_TiposPropiedad].[TIPROP_Descripcion], [tbl_Propiedades].[PROP_Calle], [tbl_Propiedades].[PROP_Nro], [tbl_Propiedades].[PROP_PisoDpto], [tbl_Propiedades].[PROP_360], [tbl_Propiedades].[PPROP_Mapa], [tbl_OperacionesPosibles].[OP_Financiacion], [tbl_Propiedades].[PROP_DescripcionGeneral], [tbl_Propiedades].[PROP_Inmobiliaria], [tbl_PARAM_Inmobiliarias].[INM_Nombre], [tbl_Propiedades].[PROP_Vendido], [tbl_PARAM_Partidos].[PART_Nombre], [tbl_PARAM_Inmobiliarias].[INM_Id], [tbl_PARAM_Inmobiliarias].[INM_Destacados], [tbl_PARAM_Inmobiliarias].[INM_Desabilitada], [tbl_PARAM_Inmobiliarias].[INM_Url], [tbl_OperacionesPosibles].[OP_DestaWebclient]
FROM (tbl_PARAM_TiposPropiedad RIGHT JOIN (tbl_PARAM_Inmobiliarias INNER JOIN ((tbl_Propiedades INNER JOIN tbl_PARAM_Localidades ON ([tbl_Propiedades].[PROP_PROV_Id]=[tbl_PARAM_Localidades].[LOCAL_PROV_Id]) AND ([tbl_Propiedades].[PROP_LOCAL_Id]=[tbl_PARAM_Localidades].[LOCAL_Id])) INNER JOIN tbl_PARAM_Partidos ON ([tbl_Propiedades].[PROP_PART_Id]=[tbl_PARAM_Partidos].[PART_Id]) AND ([tbl_Propiedades].[PROP_LOCAL_Id]=[tbl_PARAM_Partidos].[PART_LOCAL_Id]) AND ([tbl_Propiedades].[PROP_PROV_Id]=[tbl_PARAM_Partidos].[PART_PROV_Id])) ON [tbl_PARAM_Inmobiliarias].[INM_Id]=[tbl_Propiedades].[PROP_Inmobiliaria]) ON [tbl_PARAM_TiposPropiedad].[TIPROP_Id]=[tbl_Propiedades].[PROP_TIPROP_Id]) INNER JOIN (tbl_PARAM_TiposOperacion RIGHT JOIN (tbl_PARAM_Monedas RIGHT JOIN tbl_OperacionesPosibles ON [tbl_PARAM_Monedas].[MONEDAS_Id]=[tbl_OperacionesPosibles].[OP_MONEDAS_Id]) ON [tbl_PARAM_TiposOperacion].[OPER_Id]=[tbl_OperacionesPosibles].[OP_OPER_Id]) ON [tbl_Propiedades].[PROP_Id]=[tbl_OperacionesPosibles].[OP_PROP_Id]
WHERE ((([tbl_OperacionesPosibles].[OP_Destacada])=True));

CREATE VIEW [Cons_DestacadaWebclient] AS SELECT tbl_Propiedades.PROP_Id, tbl_PARAM_Localidades.LOCAL_Nombre, tbl_OperacionesPosibles.OP_DestaWebclient, tbl_Propiedades.PROP_SupTotal, tbl_OperacionesPosibles.OP_Monto, tbl_OperacionesPosibles.OP_Id, tbl_PARAM_Monedas.MONEDAS_Signo, tbl_PARAM_TiposOperacion.OPER_Descripcion, tbl_PARAM_TiposPropiedad.TIPROP_Descripcion, tbl_Propiedades.PROP_Calle, tbl_Propiedades.PROP_Nro, tbl_Propiedades.PROP_PisoDpto, tbl_Propiedades.PROP_360, tbl_Propiedades.PPROP_Mapa, tbl_OperacionesPosibles.OP_Financiacion, tbl_Propiedades.PROP_DescripcionGeneral, tbl_Propiedades.PROP_Inmobiliaria, tbl_PARAM_Inmobiliarias.INM_Nombre, tbl_Propiedades.PROP_Vendido, tbl_PARAM_Partidos.PART_Nombre, tbl_PARAM_Inmobiliarias.INM_Id, tbl_PARAM_Inmobiliarias.INM_Destacados, tbl_PARAM_Inmobiliarias.INM_Desabilitada, tbl_PARAM_Inmobiliarias.INM_Url
FROM (tbl_PARAM_TiposPropiedad RIGHT JOIN (tbl_PARAM_Inmobiliarias INNER JOIN ((tbl_Propiedades INNER JOIN tbl_PARAM_Localidades ON (tbl_Propiedades.PROP_LOCAL_Id = tbl_PARAM_Localidades.LOCAL_Id) AND (tbl_Propiedades.PROP_PROV_Id = tbl_PARAM_Localidades.LOCAL_PROV_Id)) INNER JOIN tbl_PARAM_Partidos ON (tbl_Propiedades.PROP_PROV_Id = tbl_PARAM_Partidos.PART_PROV_Id) AND (tbl_Propiedades.PROP_LOCAL_Id = tbl_PARAM_Partidos.PART_LOCAL_Id) AND (tbl_Propiedades.PROP_PART_Id = tbl_PARAM_Partidos.PART_Id)) ON tbl_PARAM_Inmobiliarias.INM_Id = tbl_Propiedades.PROP_Inmobiliaria) ON tbl_PARAM_TiposPropiedad.TIPROP_Id = tbl_Propiedades.PROP_TIPROP_Id) INNER JOIN (tbl_PARAM_TiposOperacion RIGHT JOIN (tbl_PARAM_Monedas RIGHT JOIN tbl_OperacionesPosibles ON tbl_PARAM_Monedas.MONEDAS_Id = tbl_OperacionesPosibles.OP_MONEDAS_Id) ON tbl_PARAM_TiposOperacion.OPER_Id = tbl_OperacionesPosibles.OP_OPER_Id) ON tbl_Propiedades.PROP_Id = tbl_OperacionesPosibles.OP_PROP_Id
WHERE (((tbl_OperacionesPosibles.OP_DestaWebclient)=True));

CREATE VIEW [Cons_Fotos] AS SELECT [tbl_Fotos].[Id], [tbl_Fotos].[PROP_Id], [tbl_Fotos].[Tituloimagen], [tbl_Fotos].[Titulo]
FROM tbl_Fotos
WHERE ((([tbl_Fotos].[Titulo])<>"PPAL"));

CREATE VIEW [Cons_Localidades] AS SELECT tbl_Propiedades.PROP_LOCAL_Id, tbl_PARAM_Localidades.LOCAL_Id, tbl_PARAM_Localidades.LOCAL_Nombre, tbl_PARAM_Localidades.LOCAL_PROV_Id, tbl_Propiedades.PROP_TIPROP_Id, tbl_OperacionesPosibles.OP_OPER_Id, tbl_Propiedades.PROP_Inmobiliaria
FROM (tbl_Propiedades LEFT JOIN tbl_PARAM_Localidades ON (tbl_Propiedades.PROP_PROV_Id = tbl_PARAM_Localidades.LOCAL_PROV_Id) AND (tbl_Propiedades.PROP_LOCAL_Id = tbl_PARAM_Localidades.LOCAL_Id)) RIGHT JOIN tbl_OperacionesPosibles ON tbl_Propiedades.PROP_Id = tbl_OperacionesPosibles.OP_PROP_Id;

CREATE VIEW [Cons_Monedas] AS SELECT tbl_PARAM_Monedas.MONEDAS_Id, tbl_PARAM_Monedas.MONEDAS_Descripcion, tbl_Propiedades.PROP_TIPROP_Id, tbl_OperacionesPosibles.OP_OPER_Id
FROM tbl_Propiedades RIGHT JOIN (tbl_PARAM_Monedas RIGHT JOIN tbl_OperacionesPosibles ON tbl_PARAM_Monedas.MONEDAS_Id = tbl_OperacionesPosibles.OP_MONEDAS_Id) ON tbl_Propiedades.PROP_Id = tbl_OperacionesPosibles.OP_PROP_Id;

CREATE VIEW [Cons_OperacionesPosibles] AS SELECT tbl_OperacionesPosibles.OP_Id, tbl_Propiedades.PROP_TIPROP_Id, tbl_PARAM_TiposOperacion.OPER_Descripcion, tbl_PARAM_TiposOperacion.OPER_Id, tbl_Propiedades.PROP_Inmobiliaria, tbl_OperacionesPosibles.OP_DestaWebclient, tbl_PARAM_Inmobiliarias.INM_Url
FROM (tbl_PARAM_Inmobiliarias RIGHT JOIN tbl_Propiedades ON tbl_PARAM_Inmobiliarias.INM_Id = tbl_Propiedades.PROP_Inmobiliaria) RIGHT JOIN (tbl_PARAM_TiposOperacion RIGHT JOIN (tbl_PARAM_Monedas RIGHT JOIN tbl_OperacionesPosibles ON tbl_PARAM_Monedas.MONEDAS_Id = tbl_OperacionesPosibles.OP_MONEDAS_Id) ON tbl_PARAM_TiposOperacion.OPER_Id = tbl_OperacionesPosibles.OP_OPER_Id) ON tbl_Propiedades.PROP_Id = tbl_OperacionesPosibles.OP_PROP_Id;

CREATE VIEW [Cons_Partidos] AS SELECT tbl_Propiedades.PROP_PART_Id, tbl_PARAM_Partidos.PART_Nombre, tbl_PARAM_Partidos.PART_LOCAL_Id, tbl_Propiedades.PROP_PROV_Id, tbl_Propiedades.PROP_TIPROP_Id, tbl_OperacionesPosibles.OP_OPER_Id, tbl_Propiedades.PROP_Inmobiliaria
FROM (tbl_Propiedades LEFT JOIN tbl_PARAM_Partidos ON (tbl_Propiedades.PROP_PROV_Id = tbl_PARAM_Partidos.PART_PROV_Id) AND (tbl_Propiedades.PROP_LOCAL_Id = tbl_PARAM_Partidos.PART_LOCAL_Id) AND (tbl_Propiedades.PROP_PART_Id = tbl_PARAM_Partidos.PART_Id)) RIGHT JOIN tbl_OperacionesPosibles ON tbl_Propiedades.PROP_Id = tbl_OperacionesPosibles.OP_PROP_Id;

CREATE VIEW [Cons_Provincia] AS SELECT tbl_PARAM_Provincias.PROV_Id, tbl_PARAM_Provincias.PROV_Nombre, tbl_Propiedades.PROP_TIPROP_Id, tbl_OperacionesPosibles.OP_OPER_Id, tbl_Propiedades.PROP_Inmobiliaria
FROM (tbl_PARAM_Provincias RIGHT JOIN tbl_Propiedades ON tbl_PARAM_Provincias.PROV_Id = tbl_Propiedades.PROP_PROV_Id) RIGHT JOIN tbl_OperacionesPosibles ON tbl_Propiedades.PROP_Id = tbl_OperacionesPosibles.OP_PROP_Id;

CREATE VIEW [Cons_Usuarios_Propiedades] AS SELECT tbl_Usuarios_Propiedades.Id, tbl_Usuarios_Propiedades.Usuario, tbl_Usuarios_Propiedades.OP_Id, Operaciones.OPER_Descripcion, Operaciones.PROP_Id, Operaciones.MONEDAS_Signo, Operaciones.OP_Monto, Operaciones.OP_Financiacion, Operaciones.TIPROP_Descripcion, Operaciones.PROV_Nombre, Operaciones.LOCAL_Nombre, Operaciones.PART_Nombre, Operaciones.LUGAR_Descripcion, Operaciones.PROP_barrio, Operaciones.PROP_Calle, Operaciones.PROP_Nro, Operaciones.PROP_PisoDpto, Operaciones.PROP_DireccionOtros, Operaciones.PROP_SupLibre, Operaciones.PROP_SupCubierta, Operaciones.PROP_SupTotal, Operaciones.PROP_DescripcionGeneral, Operaciones.PROP_360, Operaciones.PPROP_Mapa, Operaciones.OP_Destacada, Operaciones.INM_Id, Operaciones.INM_Nombre, tbl_Usuarios_Propiedades.Contrasena
FROM tbl_Usuarios_Propiedades LEFT JOIN Operaciones ON tbl_Usuarios_Propiedades.OP_Id = Operaciones.OP_Id;

CREATE VIEW [Operaciones] AS SELECT tbl_OperacionesPosibles.OP_Id, tbl_OperacionesPosibles.OP_OPER_Id, tbl_PARAM_TiposOperacion.OPER_Descripcion, tbl_OperacionesPosibles.OP_MONEDAS_Id, tbl_PARAM_Monedas.MONEDAS_Signo, tbl_OperacionesPosibles.OP_Monto, tbl_OperacionesPosibles.OP_Expensas, tbl_OperacionesPosibles.OP_Financiacion, tbl_OperacionesPosibles.OP_Financiacion_detalle, tbl_Propiedades.PROP_Id, tbl_Propiedades.PROP_TIPROP_Id, tbl_PARAM_TiposPropiedad.TIPROP_Descripcion, tbl_Propiedades.PROP_PROV_Id, tbl_PARAM_Provincias.PROV_Nombre, tbl_Propiedades.PROP_LOCAL_Id, tbl_PARAM_Localidades.LOCAL_Nombre, tbl_Propiedades.PROP_PART_Id, tbl_PARAM_Partidos.PART_Nombre, tbl_PARAM_Lugar.LUGAR_Id, tbl_PARAM_Lugar.LUGAR_Descripcion, tbl_Propiedades.PROP_barrio, tbl_Propiedades.PROP_Calle, tbl_Propiedades.PROP_Nro, tbl_Propiedades.PROP_PisoDpto, tbl_Propiedades.PROP_DireccionOtros, tbl_Propiedades.PROP_ServAgua, tbl_Propiedades.PROP_ServLuz, tbl_Propiedades.PROP_ServGasNatural, tbl_Propiedades.PROP_ServGasGarrafa, tbl_Propiedades.PROP_ServCloacas, tbl_Propiedades.PROP_ServCable, tbl_Propiedades.PROP_ServTelefono, tbl_Propiedades.PROP_SupLibre, tbl_Propiedades.PROP_SupCubierta, tbl_Propiedades.PROP_SupTotal, tbl_Propiedades.PROP_Dormitorios, tbl_Propiedades.PROP_Plantas, tbl_Propiedades.PROP_Ambientes, tbl_Propiedades.PROP_Antiguedad, tbl_Propiedades.PROP_Banos, tbl_Propiedades.PROP_Edificacion, tbl_Propiedades.PROP_Amoblado, tbl_Propiedades.PROP_Cochera, tbl_Propiedades.PROP_Dependencia, tbl_Propiedades.PROP_Parque, tbl_Propiedades.PROP_VMF, tbl_Propiedades.PROP_Patio, tbl_Propiedades.PROP_Pileta, tbl_Propiedades.PROP_Asfalto, tbl_Propiedades.PROP_Terraza, tbl_Propiedades.PROP_DescripcionGeneral, tbl_Propiedades.PROP_FechaIngreso, tbl_PARAM_TiposPropiedad.imagenboton, tbl_PARAM_TiposPropiedad.imagenbotonv, tbl_Propiedades.PROP_360, tbl_Propiedades.PPROP_Mapa, tbl_OperacionesPosibles.OP_Destacada, tbl_PARAM_Inmobiliarias.INM_Id, tbl_PARAM_Inmobiliarias.INM_Nombre, tbl_PARAM_Inmobiliarias.INM_Email, tbl_Propiedades.PROP_Vendido, tbl_PARAM_Inmobiliarias.INM_Destacados, tbl_PARAM_Inmobiliarias.INM_Desabilitada
FROM (tbl_PARAM_TiposPropiedad RIGHT JOIN (tbl_PARAM_Lugar RIGHT JOIN (tbl_PARAM_Inmobiliarias RIGHT JOIN (((tbl_PARAM_Provincias RIGHT JOIN tbl_Propiedades ON tbl_PARAM_Provincias.PROV_Id = tbl_Propiedades.PROP_PROV_Id) LEFT JOIN tbl_PARAM_Localidades ON (tbl_Propiedades.PROP_PROV_Id = tbl_PARAM_Localidades.LOCAL_PROV_Id) AND (tbl_Propiedades.PROP_LOCAL_Id = tbl_PARAM_Localidades.LOCAL_Id)) LEFT JOIN tbl_PARAM_Partidos ON (tbl_Propiedades.PROP_PROV_Id = tbl_PARAM_Partidos.PART_PROV_Id) AND (tbl_Propiedades.PROP_LOCAL_Id = tbl_PARAM_Partidos.PART_LOCAL_Id) AND (tbl_Propiedades.PROP_PART_Id = tbl_PARAM_Partidos.PART_Id)) ON tbl_PARAM_Inmobiliarias.INM_Id = tbl_Propiedades.PROP_Inmobiliaria) ON tbl_PARAM_Lugar.LUGAR_Id = tbl_Propiedades.PROP_Lugar) ON tbl_PARAM_TiposPropiedad.TIPROP_Id = tbl_Propiedades.PROP_TIPROP_Id) RIGHT JOIN (tbl_PARAM_TiposOperacion RIGHT JOIN (tbl_PARAM_Monedas RIGHT JOIN tbl_OperacionesPosibles ON tbl_PARAM_Monedas.MONEDAS_Id = tbl_OperacionesPosibles.OP_MONEDAS_Id) ON tbl_PARAM_TiposOperacion.OPER_Id = tbl_OperacionesPosibles.OP_OPER_Id) ON tbl_Propiedades.PROP_Id = tbl_OperacionesPosibles.OP_PROP_Id;

CREATE VIEW [~sq_cform boludo~sq_cCuadro combinado45] AS SELECT [tbl_PARAM_TiposPropiedad].[TIPROP_Id], [tbl_PARAM_TiposPropiedad].[TIPROP_Descripcion]
FROM tbl_PARAM_TiposPropiedad;

CREATE VIEW [~sq_cform boludo~sq_cCuadro combinado49] AS SELECT [tbl_PARAM_Provincias].[PROV_Id], [tbl_PARAM_Provincias].[PROV_Nombre]
FROM tbl_PARAM_Provincias;

CREATE PROCEDURE [~sq_cform boludo~sq_cSecundario44_4] (__PROP_Id Value) AS 
SELECT DISTINCTROW *
FROM tbl_OperacionesPosibles AS [form boludo]
WHERE ([__PROP_Id] = OP_PROP_Id);

