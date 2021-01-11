using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using MissionPlanner.Utilities;
using MissionPlanner.Controls;
using System.IO;
using System.Windows.Forms;
using System.Diagnostics;
using MissionPlanner;
using System.Drawing;

// this example taken from https://discuss.ardupilot.org/t/adding-mission-parts-at-the-beginning-and-end-of-new-mission/56579/12
// modified for this sample

namespace Aerobridge
{
    public class Plugin : MissionPlanner.Plugin.Plugin
    {
        ToolStripMenuItem but;
        MissionPlanner.Controls.MyDataGridView commands;

        public override string Name
        {
            get { return "Aerobridge Connector"; }
        }

        public override string Version
        {
            get { return "0.10"; }
        }

        public override string Author
        {
            get { return "Openskies Aerial Technology Limited"; }
        }

        public override bool Init()
        {
            return true;
        }

        public override bool Loaded()
        {
            but = new ToolStripMenuItem("Aerobridge");
            but.Click += but_Click;
            ToolStripItemCollection col = Host.FPMenuMap.Items;
            col.Add(but);
            commands =
                Host.MainForm.FlightPlanner.Controls.Find("Commands", true).FirstOrDefault() as
                    MissionPlanner.Controls.MyDataGridView;
            return true;
        }

        public override bool Loop()
        {
            return true;
        }

        public override bool Exit()
        {
            return true;
        }

        void but_Click(object sender, EventArgs e)
        {


            //Add intro and some warnings
            // CustomMessageBox.Show("This plugin will connect to a Aerobridge Server Instance.\r\n\r\n" +
            //                       "Please make sure you have the proper credentials for Aerobridge first.\r\n", "Welcome to Aerobridge");


            // if (!Host.cs.connected)
            // {
            //     CustomMessageBox.Show("Please connect first!", "Initial paremeter calculator", MessageBoxButtons.OK, MessageBoxIcon.Error);
            //     return;
            // }
            string angle = "0";
            InputQuery("Aerobridge Management Server", "Choose a interaction with GCS", ref angle);
            int angle_in_number = Int32.Parse(angle);

            Host.InsertWP(0, MAVLink.MAV_CMD.DO_SET_SERVO, 9, angle_in_number, 0, 0, 0, 0, 0);
            Host.InsertWP(1, MAVLink.MAV_CMD.DO_SET_SERVO, 10, 1000, 0, 0, 0, 0, 0);

            Host.AddWPtoList(MAVLink.MAV_CMD.DO_SET_SERVO, 9, 1000, 0, 0, 0, 0, 0);
            Host.AddWPtoList(MAVLink.MAV_CMD.DO_SET_SERVO, 10, 1000, 0, 0, 0, 0, 0);

            commands.Rows.RemoveAt(1);
        }

        //// Utilities.... 
        public static Boolean InputQuery(String caption, String prompt, ref String value)
        {
            Form form;
            form = new Form();
            form.AutoScaleMode = AutoScaleMode.Font;
            //form.Font = MissionPlanner.Drawing.SystemFonts.IconTitleFont;

            SizeF dialogUnits;
            dialogUnits = form.AutoScaleDimensions;

            form.FormBorderStyle = FormBorderStyle.FixedDialog;
            form.MinimizeBox = false;
            form.MaximizeBox = false;
            form.Text = caption;

            form.ClientSize = new Size(
                        MulDiv(280, (int)dialogUnits.Width, 4),
                        MulDiv(100, (int)dialogUnits.Height, 8));

            form.StartPosition = FormStartPosition.CenterScreen;

            System.Windows.Forms.Label lblPrompt;
            lblPrompt = new System.Windows.Forms.Label();
            lblPrompt.Parent = form;
            lblPrompt.AutoSize = true;
            lblPrompt.Left = MulDiv(8, (int)dialogUnits.Width, 4);
            lblPrompt.Top = MulDiv(8, (int)dialogUnits.Height, 8);
            lblPrompt.Text = prompt;

            System.Windows.Forms.TextBox edInput;
            edInput = new System.Windows.Forms.TextBox();
            edInput.Parent = form;
            edInput.Left = lblPrompt.Left;
            edInput.Top = MulDiv(19, (int)dialogUnits.Height, 8);
            edInput.Width = MulDiv(164, (int)dialogUnits.Width, 4);
            edInput.Text = value;
            edInput.SelectAll();

            int buttonTop = MulDiv(41, (int)dialogUnits.Height, 8);
            //Command buttons should be 50x14 dlus
            Size buttonSize = new Size(50 * (int)dialogUnits.Width / 3, 14 * (int)dialogUnits.Height / 6);

            System.Windows.Forms.Button bbOk = new System.Windows.Forms.Button();
            bbOk.Parent = form;
            bbOk.Text = "Get Drone ID";
            bbOk.Location = new Point(MulDiv(10, (int)dialogUnits.Width, 4), buttonTop);
            bbOk.Size = buttonSize;

            System.Windows.Forms.Button bbCancel = new System.Windows.Forms.Button();
            bbCancel.Parent = form;
            bbCancel.Text = "Generate Public Key";
            bbCancel.Location = new Point(MulDiv(80, (int)dialogUnits.Width, 4), buttonTop);
            bbCancel.Size = buttonSize;


            System.Windows.Forms.Button requestPermArtefact = new System.Windows.Forms.Button();
            requestPermArtefact.Parent = form;
            requestPermArtefact.Text = "Request Permission Aretefact from Aerobridge";
            requestPermArtefact.Location = new Point(MulDiv(160, (int)dialogUnits.Width, 4), buttonTop);
            requestPermArtefact.Size = buttonSize;

            System.Windows.Forms.Button uploadPermissionArtefact = new System.Windows.Forms.Button();
            uploadPermissionArtefact.Parent = form;
            uploadPermissionArtefact.Text = "Upload Permission Aretfact to GCS";
            uploadPermissionArtefact.Location = new Point(MulDiv(240, (int)dialogUnits.Width, 4), buttonTop);
            uploadPermissionArtefact.Size = buttonSize;

            System.Windows.Forms.Button getSignedLogsfromGCS = new System.Windows.Forms.Button();
            getSignedLogsfromGCS.Parent = form;
            getSignedLogsfromGCS.Text = "Get Signed Logs from GCS";
            getSignedLogsfromGCS.Location = new Point(MulDiv(320, (int)dialogUnits.Width, 4), buttonTop);
            getSignedLogsfromGCS.Size = buttonSize;


            System.Windows.Forms.Button uploadSignedLogstoAerobridge = new System.Windows.Forms.Button();
            uploadSignedLogstoAerobridge.Parent = form;
            uploadSignedLogstoAerobridge.Text = "Upload Signed Logs to Aerobridge";
            uploadSignedLogstoAerobridge.Location = new Point(MulDiv(380, (int)dialogUnits.Width, 4), buttonTop);
            uploadSignedLogstoAerobridge.Size = buttonSize;

            if (form.ShowDialog() == DialogResult.OK)
            {
                value = edInput.Text;
                return true;
            }
            else
            {
                return false;
            }
        }
        public static int MulDiv(int nNumber, int nNumerator, int nDenominator)
        {
            return (int)Math.Round((float)nNumber * nNumerator / nDenominator);
        }

    }
}