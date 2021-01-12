namespace AerobridgeClient
{
    partial class aerobridgeclient
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            this.CMB_comport = new System.Windows.Forms.ComboBox();
            this.cmb_baudrate = new System.Windows.Forms.ComboBox();
            this.but_connect = new System.Windows.Forms.Button();
            this.but_armdisarm = new System.Windows.Forms.Button();
            this.serialPort1 = new System.IO.Ports.SerialPort(this.components);
            this.but_mission = new System.Windows.Forms.Button();
            this.getDroneIDBtn = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.connectorLogsLabel = new System.Windows.Forms.Label();
            this.generateKeysBtn = new System.Windows.Forms.Button();
            this.sendPermissionBtn = new System.Windows.Forms.Button();
            this.getSignedLogBtn = new System.Windows.Forms.Button();
            this.gcsOpeationsLabel = new System.Windows.Forms.Label();
            this.aerobridgeOpsLabel = new System.Windows.Forms.Label();
            this.upldSignedLogBtn = new System.Windows.Forms.Button();
            this.dwnldPermArtBtn = new System.Windows.Forms.Button();
            this.getPublicKeyBtn = new System.Windows.Forms.Button();
            this.postDroneIDRegBtn = new System.Windows.Forms.Button();
            this.jwtToken = new System.Windows.Forms.TextBox();
            this.jwtTokenLbl = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // CMB_comport
            // 
            this.CMB_comport.FormattingEnabled = true;
            this.CMB_comport.Location = new System.Drawing.Point(13, 13);
            this.CMB_comport.Name = "CMB_comport";
            this.CMB_comport.Size = new System.Drawing.Size(121, 21);
            this.CMB_comport.TabIndex = 0;
            this.CMB_comport.Click += new System.EventHandler(this.CMB_comport_Click);
            // 
            // cmb_baudrate
            // 
            this.cmb_baudrate.FormattingEnabled = true;
            this.cmb_baudrate.Items.AddRange(new object[] {
            "9600",
            "14400",
            "19200",
            "28800",
            "38400",
            "57600",
            "115200"});
            this.cmb_baudrate.Location = new System.Drawing.Point(140, 12);
            this.cmb_baudrate.Name = "cmb_baudrate";
            this.cmb_baudrate.Size = new System.Drawing.Size(121, 21);
            this.cmb_baudrate.TabIndex = 1;
            // 
            // but_connect
            // 
            this.but_connect.Location = new System.Drawing.Point(268, 12);
            this.but_connect.Name = "but_connect";
            this.but_connect.Size = new System.Drawing.Size(75, 23);
            this.but_connect.TabIndex = 2;
            this.but_connect.Text = "Connect";
            this.but_connect.UseVisualStyleBackColor = true;
            this.but_connect.Click += new System.EventHandler(this.but_connect_Click);
            // 
            // but_armdisarm
            // 
            this.but_armdisarm.Location = new System.Drawing.Point(452, 12);
            this.but_armdisarm.Name = "but_armdisarm";
            this.but_armdisarm.Size = new System.Drawing.Size(75, 23);
            this.but_armdisarm.TabIndex = 3;
            this.but_armdisarm.Text = "Arm/Disarm";
            this.but_armdisarm.UseVisualStyleBackColor = true;
            this.but_armdisarm.Click += new System.EventHandler(this.but_armdisarm_Click);
            // 
            // but_mission
            // 
            this.but_mission.Location = new System.Drawing.Point(349, 12);
            this.but_mission.Name = "but_mission";
            this.but_mission.Size = new System.Drawing.Size(97, 23);
            this.but_mission.TabIndex = 4;
            this.but_mission.Text = "Send Mission";
            this.but_mission.UseVisualStyleBackColor = true;
            this.but_mission.Click += new System.EventHandler(this.but_mission_Click);
            // 
            // getDroneIDBtn
            // 
            this.getDroneIDBtn.Location = new System.Drawing.Point(13, 105);
            this.getDroneIDBtn.Name = "getDroneIDBtn";
            this.getDroneIDBtn.Size = new System.Drawing.Size(104, 23);
            this.getDroneIDBtn.TabIndex = 5;
            this.getDroneIDBtn.Text = "Get Drone ID";
            this.getDroneIDBtn.UseVisualStyleBackColor = true;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(32, 314);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(0, 13);
            this.label1.TabIndex = 6;
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(13, 276);
            this.textBox1.Multiline = true;
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(330, 190);
            this.textBox1.TabIndex = 7;
            // 
            // connectorLogsLabel
            // 
            this.connectorLogsLabel.AutoSize = true;
            this.connectorLogsLabel.Location = new System.Drawing.Point(12, 260);
            this.connectorLogsLabel.Name = "connectorLogsLabel";
            this.connectorLogsLabel.Size = new System.Drawing.Size(30, 13);
            this.connectorLogsLabel.TabIndex = 8;
            this.connectorLogsLabel.Text = "Logs";
            // this.connectorLogsLabel.Click += new System.EventHandler(this.label2_Click);
            // 
            // generateKeysBtn
            // 
            this.generateKeysBtn.Location = new System.Drawing.Point(13, 145);
            this.generateKeysBtn.Name = "generateKeysBtn";
            this.generateKeysBtn.Size = new System.Drawing.Size(104, 23);
            this.generateKeysBtn.TabIndex = 9;
            this.generateKeysBtn.Text = "Generate Keys";
            this.generateKeysBtn.UseVisualStyleBackColor = true;
            // 
            // sendPermissionBtn
            // 
            this.sendPermissionBtn.Location = new System.Drawing.Point(13, 183);
            this.sendPermissionBtn.Name = "sendPermissionBtn";
            this.sendPermissionBtn.Size = new System.Drawing.Size(105, 23);
            this.sendPermissionBtn.TabIndex = 10;
            this.sendPermissionBtn.Text = "Send Permission Artefact";
            this.sendPermissionBtn.UseVisualStyleBackColor = true;
            // this.sendPermissionBtn.Click += new System.EventHandler(this.button2_Click);
            // 
            // getSignedLogBtn
            // 
            this.getSignedLogBtn.Location = new System.Drawing.Point(12, 223);
            this.getSignedLogBtn.Name = "getSignedLogBtn";
            this.getSignedLogBtn.Size = new System.Drawing.Size(105, 23);
            this.getSignedLogBtn.TabIndex = 11;
            this.getSignedLogBtn.Text = "Get Signed Log";
            this.getSignedLogBtn.UseVisualStyleBackColor = true;
            // this.getSignedLogBtn.Click += new System.EventHandler(this.button3_Click);
            // 
            // gcsOpeationsLabel
            // 
            this.gcsOpeationsLabel.AutoSize = true;
            this.gcsOpeationsLabel.Location = new System.Drawing.Point(12, 76);
            this.gcsOpeationsLabel.Name = "gcsOpeationsLabel";
            this.gcsOpeationsLabel.Size = new System.Drawing.Size(84, 13);
            this.gcsOpeationsLabel.TabIndex = 12;
            this.gcsOpeationsLabel.Text = "RFM Operations";
            // 
            // aerobridgeOpsLabel
            // 
            this.aerobridgeOpsLabel.AutoSize = true;
            this.aerobridgeOpsLabel.Location = new System.Drawing.Point(346, 76);
            this.aerobridgeOpsLabel.Name = "aerobridgeOpsLabel";
            this.aerobridgeOpsLabel.Size = new System.Drawing.Size(112, 13);
            this.aerobridgeOpsLabel.TabIndex = 17;
            this.aerobridgeOpsLabel.Text = "Aerobridge Operations";
            // 
            // upldSignedLogBtn
            // 
            this.upldSignedLogBtn.Location = new System.Drawing.Point(346, 223);
            this.upldSignedLogBtn.Name = "upldSignedLogBtn";
            this.upldSignedLogBtn.Size = new System.Drawing.Size(232, 23);
            this.upldSignedLogBtn.TabIndex = 16;
            this.upldSignedLogBtn.Text = "Upload Signed Log";
            this.upldSignedLogBtn.UseVisualStyleBackColor = true;
            // 
            // dwnldPermArtBtn
            // 
            this.dwnldPermArtBtn.Location = new System.Drawing.Point(347, 183);
            this.dwnldPermArtBtn.Name = "dwnldPermArtBtn";
            this.dwnldPermArtBtn.Size = new System.Drawing.Size(231, 23);
            this.dwnldPermArtBtn.TabIndex = 15;
            this.dwnldPermArtBtn.Text = "Download Permission Artefact";
            this.dwnldPermArtBtn.UseVisualStyleBackColor = true;
            // 
            // getPublicKeyBtn
            // 
            this.getPublicKeyBtn.Location = new System.Drawing.Point(347, 145);
            this.getPublicKeyBtn.Name = "getPublicKeyBtn";
            this.getPublicKeyBtn.Size = new System.Drawing.Size(231, 23);
            this.getPublicKeyBtn.TabIndex = 14;
            this.getPublicKeyBtn.Text = "Get Signed Public Key and UUID";
            this.getPublicKeyBtn.UseVisualStyleBackColor = true;
            // 
            // postDroneIDRegBtn
            // 
            this.postDroneIDRegBtn.Location = new System.Drawing.Point(347, 105);
            this.postDroneIDRegBtn.Name = "postDroneIDRegBtn";
            this.postDroneIDRegBtn.Size = new System.Drawing.Size(231, 23);
            this.postDroneIDRegBtn.TabIndex = 13;
            this.postDroneIDRegBtn.Text = "Post Drone ID and Public Key for registration";
            this.postDroneIDRegBtn.UseVisualStyleBackColor = true;
            // 
            // jwtToken
            // 
            this.jwtToken.Location = new System.Drawing.Point(349, 276);
            this.jwtToken.Multiline = true;
            this.jwtToken.Name = "jwtToken";
            this.jwtToken.Size = new System.Drawing.Size(247, 190);
            this.jwtToken.TabIndex = 18;
            // 
            // jwtTokenLbl
            // 
            this.jwtTokenLbl.AutoSize = true;
            this.jwtTokenLbl.Location = new System.Drawing.Point(346, 260);
            this.jwtTokenLbl.Name = "jwtTokenLbl";
            this.jwtTokenLbl.Size = new System.Drawing.Size(118, 13);
            this.jwtTokenLbl.TabIndex = 19;
            this.jwtTokenLbl.Text = "Aerobridge JWT Token";
            // 
            // aerobridgeclient
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(608, 478);
            this.Controls.Add(this.jwtTokenLbl);
            this.Controls.Add(this.jwtToken);
            this.Controls.Add(this.aerobridgeOpsLabel);
            this.Controls.Add(this.upldSignedLogBtn);
            this.Controls.Add(this.dwnldPermArtBtn);
            this.Controls.Add(this.getPublicKeyBtn);
            this.Controls.Add(this.postDroneIDRegBtn);
            this.Controls.Add(this.gcsOpeationsLabel);
            this.Controls.Add(this.getSignedLogBtn);
            this.Controls.Add(this.sendPermissionBtn);
            this.Controls.Add(this.generateKeysBtn);
            this.Controls.Add(this.connectorLogsLabel);
            this.Controls.Add(this.textBox1);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.getDroneIDBtn);
            this.Controls.Add(this.but_mission);
            this.Controls.Add(this.but_armdisarm);
            this.Controls.Add(this.but_connect);
            this.Controls.Add(this.cmb_baudrate);
            this.Controls.Add(this.CMB_comport);
            this.Name = "aerobridgeclient";
            this.Text = "Aerobridge RFM Conector";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ComboBox CMB_comport;
        private System.Windows.Forms.ComboBox cmb_baudrate;
        private System.Windows.Forms.Button but_connect;
        private System.Windows.Forms.Button but_armdisarm;
        private System.IO.Ports.SerialPort serialPort1;
        private System.Windows.Forms.Button but_mission;
        private System.Windows.Forms.Button getDroneIDBtn;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.Label connectorLogsLabel;
        private System.Windows.Forms.Button generateKeysBtn;
        private System.Windows.Forms.Button sendPermissionBtn;
        private System.Windows.Forms.Button getSignedLogBtn;
        private System.Windows.Forms.Label gcsOpeationsLabel;
        private System.Windows.Forms.Label aerobridgeOpsLabel;
        private System.Windows.Forms.Button upldSignedLogBtn;
        private System.Windows.Forms.Button dwnldPermArtBtn;
        private System.Windows.Forms.Button getPublicKeyBtn;
        private System.Windows.Forms.Button postDroneIDRegBtn;
        private System.Windows.Forms.TextBox jwtToken;
        private System.Windows.Forms.Label jwtTokenLbl;
    }
}

