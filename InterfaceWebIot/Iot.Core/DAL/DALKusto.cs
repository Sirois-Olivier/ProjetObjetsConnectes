using Azure.Identity;
using Kusto.Data.Common;
using Kusto.Data.Net.Client;
using Kusto.Data;
using System;
using System.Collections.Generic;
using System.Diagnostics.Metrics;
using System.Linq;
using System.Security.Policy;
using System.Text;
using System.Threading.Tasks;
using Kusto.Cloud.Platform.Data;
using System.IO;
using System.Text.Json;
using Iot.Core.DLL;

namespace Iot.Core.DAL
{
    public static class DALKusto
    {
        static KustoConnectionStringBuilder builder = new KustoConnectionStringBuilder("https://clusterserre.eastus2.kusto.windows.net/databaseserre");

        public static DLLTemperatureDate GetData()
        {

            //var client = Kusto.Data.Net.Client.KustoClientFactory.CreateCslQueryProvider(builder);
            //var query = $@"tableserre | count";
            //var reader = client.ExecuteQuery(query);

            //var array = reader.ToEnumerableObjectArray();

            //reader.Close();

        
            string jsonString = File.ReadAllText(Environment.GetFolderPath(Environment.SpecialFolder.MyDocuments) + "/donneesSimulees.json");

            DLLTemperatureDate dLLTemperatureDate = JsonSerializer.Deserialize<DLLTemperatureDate>(jsonString);

            return dLLTemperatureDate;
        }  
    }
}
