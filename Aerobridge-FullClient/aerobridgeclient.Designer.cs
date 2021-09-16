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
            this.label1 = new System.Windows.Forms.Label();
            this.textBox1 = new System.Windows.Forms.TextBox();
            this.connectorLogsLabel = new System.Windows.Forms.Label();
            this.aerobridgeOpsLabel = new System.Windows.Forms.Label();
            this.dwnldPermArtBtn = new System.Windows.Forms.Button();
            this.jwtToken = new System.Windows.Forms.TextBox();
            this.jwtTokenLbl = new System.Windows.Forms.Label();
            this.flightOperations = new System.Windows.Forms.ComboBox();
            this.button1 = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // CMB_comport
            // 
            this.CMB_comport.FormattingEnabled = true;
            this.CMB_comport.Location = new System.Drawing.Point(17, 16);
            this.CMB_comport.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.CMB_comport.Name = "CMB_comport";
            this.CMB_comport.Size = new System.Drawing.Size(160, 24);
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
            this.cmb_baudrate.Location = new System.Drawing.Point(187, 15);
            this.cmb_baudrate.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.cmb_baudrate.Name = "cmb_baudrate";
            this.cmb_baudrate.Size = new System.Drawing.Size(160, 24);
            this.cmb_baudrate.TabIndex = 1;
            // 
            // but_connect
            // 
            this.but_connect.Location = new System.Drawing.Point(357, 15);
            this.but_connect.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.but_connect.Name = "but_connect";
            this.but_connect.Size = new System.Drawing.Size(100, 28);
            this.but_connect.TabIndex = 2;
            this.but_connect.Text = "Connect";
            this.but_connect.UseVisualStyleBackColor = true;
            this.but_connect.Click += new System.EventHandler(this.but_connect_Click);
            // 
            // but_armdisarm
            // 
            this.but_armdisarm.Location = new System.Drawing.Point(465, 15);
            this.but_armdisarm.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.but_armdisarm.Name = "but_armdisarm";
            this.but_armdisarm.Size = new System.Drawing.Size(100, 28);
            this.but_armdisarm.TabIndex = 3;
            this.but_armdisarm.Text = "Arm/Disarm";
            this.but_armdisarm.UseVisualStyleBackColor = true;
            this.but_armdisarm.Click += new System.EventHandler(this.but_armdisarm_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(43, 386);
            this.label1.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(0, 17);
            this.label1.TabIndex = 6;
            // 
            // textBox1
            // 
            this.textBox1.Location = new System.Drawing.Point(357, 228);
            this.textBox1.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.textBox1.Multiline = true;
            this.textBox1.Name = "textBox1";
            this.textBox1.Size = new System.Drawing.Size(439, 347);
            this.textBox1.TabIndex = 7;
            this.textBox1.Text = "Drone Communication Logs are here...";
            // 
            // connectorLogsLabel
            // 
            this.connectorLogsLabel.AutoSize = true;
            this.connectorLogsLabel.Location = new System.Drawing.Point(354, 194);
            this.connectorLogsLabel.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.connectorLogsLabel.Name = "connectorLogsLabel";
            this.connectorLogsLabel.Size = new System.Drawing.Size(39, 17);
            this.connectorLogsLabel.TabIndex = 8;
            this.connectorLogsLabel.Text = "Logs";
            // 
            // aerobridgeOpsLabel
            // 
            this.aerobridgeOpsLabel.AutoSize = true;
            this.aerobridgeOpsLabel.Location = new System.Drawing.Point(16, 62);
            this.aerobridgeOpsLabel.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.aerobridgeOpsLabel.Name = "aerobridgeOpsLabel";
            this.aerobridgeOpsLabel.Size = new System.Drawing.Size(82, 17);
            this.aerobridgeOpsLabel.TabIndex = 17;
            this.aerobridgeOpsLabel.Text = "Pre-mission";
            this.aerobridgeOpsLabel.Click += new System.EventHandler(this.aerobridgeOpsLabel_Click);
            // 
            // dwnldPermArtBtn
            // 
            this.dwnldPermArtBtn.Location = new System.Drawing.Point(17, 125);
            this.dwnldPermArtBtn.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.dwnldPermArtBtn.Name = "dwnldPermArtBtn";
            this.dwnldPermArtBtn.Size = new System.Drawing.Size(259, 28);
            this.dwnldPermArtBtn.TabIndex = 15;
            this.dwnldPermArtBtn.Text = "Download Permission Artefact";
            this.dwnldPermArtBtn.UseVisualStyleBackColor = true;
            // 
            // jwtToken
            // 
            this.jwtToken.Location = new System.Drawing.Point(357, 83);
            this.jwtToken.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
            this.jwtToken.Multiline = true;
            this.jwtToken.Name = "jwtToken";
            this.jwtToken.Size = new System.Drawing.Size(441, 95);
            this.jwtToken.TabIndex = 18;
            this.jwtToken.Text = "Paste JWT Token here...";
            // 
            // jwtTokenLbl
            // 
            this.jwtTokenLbl.AutoSize = true;
            this.jwtTokenLbl.Location = new System.Drawing.Point(354, 62);
            this.jwtTokenLbl.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.jwtTokenLbl.Name = "jwtTokenLbl";
            this.jwtTokenLbl.Size = new System.Drawing.Size(155, 17);
            this.jwtTokenLbl.TabIndex = 19;
            this.jwtTokenLbl.Text = "Aerobridge JWT Token";
            // 
            // flightOperations
            // 
            this.flightOperations.FormattingEnabled = true;
            this.flightOperations.Items.AddRange(new object[] {
            "9600",
            "14400",
            "19200",
            "28800",
            "38400",
            "57600",
            "115200"});
            this.flightOperations.Location = new System.Drawing.Point(19, 83);
            this.flightOperations.Margin = new System.Windows.Forms.Padding(4);
            this.flightOperations.Name = "flightOperations";
            this.flightOperations.Size = new System.Drawing.Size(174, 24);
            this.flightOperations.TabIndex = 20;
            // 
            // button1
            // 
            this.button1.Location = new System.Drawing.Point(19, 252);
            this.button1.Margin = new System.Windows.Forms.Padding(4);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(174, 28);
            this.button1.TabIndex = 21;
            this.button1.Text = "Upload Flight Log";
            this.button1.UseVisualStyleBackColor = true;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(16, 228);
            this.label2.Margin = new System.Windows.Forms.Padding(4, 0, 4, 0);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(82, 17);
            this.label2.TabIndex = 22;
            this.label2.Text = "Pre-mission";
            this.label2.Click += new System.EventHandler(this.label2_Click);
            // 
            // aerobridgeclient
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(8F, 16F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(811, 588);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.button1);
            this.Controls.Add(this.flightOperations);
            this.Controls.Add(this.jwtTokenLbl);
            this.Controls.Add(this.jwtToken);
            this.Controls.Add(this.aerobridgeOpsLabel);
            this.Controls.Add(this.dwnldPermArtBtn);
            this.Controls.Add(this.connectorLogsLabel);
            this.Controls.Add(this.textBox1);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.but_armdisarm);
            this.Controls.Add(this.but_connect);
            this.Controls.Add(this.cmb_baudrate);
            this.Controls.Add(this.CMB_comport);
            this.Margin = new System.Windows.Forms.Padding(4, 4, 4, 4);
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
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.TextBox textBox1;
        private System.Windows.Forms.Label connectorLogsLabel;
        private System.Windows.Forms.Label aerobridgeOpsLabel;
        private System.Windows.Forms.Button dwnldPermArtBtn;
        private System.Windows.Forms.TextBox jwtToken;
        private System.Windows.Forms.Label jwtTokenLbl;
        private System.Windows.Forms.ComboBox flightOperations;
        private System.Windows.Forms.Button button1;
        private System.Windows.Forms.Label label2;
    }
}

