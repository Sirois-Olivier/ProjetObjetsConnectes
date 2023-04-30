using Microsoft.Azure.Devices;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Iot.Core.BLL
{
    public class BLLAzureIotManager
    {
        public async Task SendMessageToAzure()
        {
            ServiceClient srv;
            string connectionString = "HostName=iothubserre.azure-devices.net;DeviceId=deviceserre;SharedAccessKey=BDWKJV/+KR6BKaWZsIHGdThmvT/jFy5Wi91ZxSstolQ=";
            string targetDevice = "deviceserre";

            var msg = new Message(Encoding.ASCII.GetBytes("Cloud to device message."));
            srv = ServiceClient.CreateFromConnectionString(connectionString);
            await srv.SendAsync(targetDevice, msg);

            
        }
    }
}
