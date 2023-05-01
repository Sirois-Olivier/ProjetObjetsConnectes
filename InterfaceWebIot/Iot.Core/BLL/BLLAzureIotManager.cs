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
        public Task SendMessageToAzure(string method, string param)
        {
            ServiceClient srv;
            string connectionString = "HostName=iothubserre.azure-devices.net;SharedAccessKeyName=service;SharedAccessKey=rYaRsuzeuUj8+SS5sHGZeToGym+Mdm6dMNYIKwmilBc=";
            string targetDevice = "deviceserre";

            srv = ServiceClient.CreateFromConnectionString(connectionString);
            CloudToDeviceMethod cloudToDeviceMethod = new CloudToDeviceMethod(String.Format("{0},{1}", method, param));
            cloudToDeviceMethod.ResponseTimeout = TimeSpan.FromSeconds(30);

            return srv.InvokeDeviceMethodAsync(targetDevice, cloudToDeviceMethod);

        }
    }
}
