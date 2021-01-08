/*
 * This is a sample plugin frame work for Mission Planner 
 * 
*/


using System;
using System.Collections.Generic;
using System.Linq;
using MissionPlanner.Utilities;
using System.Reactive.Linq;
using System.Windows.Forms;
using MissionPlanner.Controls;

namespace MissionPlanner.AerobridgeConnector
{
    public class AerobridgePlugin : MissionPlanner.Plugin.Plugin
    {

        //Additional variables 
        MissionPlanner.Controls.pingButton button;

        public override string Name
        {
            get { return "Misson Planner Aerobridge Plugin"; }
        }

        public override string Version
        {
            get { return "1.0" }
        }

        public override string Author
        {
            get { return "Openskies Aerial Technology Ltd."; }
        }

        public override bool Init()
        {
            return true;
        }

        public override bool Loaded()
        {

            return true;
        }

        private bool Instance_ProcessCmdKeyCallback(ref System.Windows.Forms.Message msg, System.Windows.Forms.Keys keyData)
        {

            //Add our shortcut (Alt + I) 

            if (keyData == (Keys.Alt | Keys.I))
            {
                launch_welcome(this, null);
                return true;
            }
            return false;
        }

        // Main 
        void launch_welcome(object sender, EventArgs e)
        {
            //Add intro and some warnings
            CustomMessageBox.Show("This plugin will connect to a Aerobridge Server Instance.\r\n\r\n" +
                                  "Please make sure you have the proper credentials for Aerobridge first.\r\n", "Welcome to Aerobridge");


            if (!Host.cs.connected)
            {
                CustomMessageBox.Show("Please connect first!", "Initial paremeter calculator", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
        }

        public override bool Exit()
        {
            return true;
        }
    }
}
