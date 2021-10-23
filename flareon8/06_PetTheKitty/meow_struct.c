#include <stdio.h>
#include <windows.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <msdelta.h>
#pragma comment(lib, "msdelta.lib")
typedef struct _MEOW
{
    DWORD dwHeader;
    DWORD dataSize;
    DWORD PatchSize;
    BYTE data[1];
} MEOW, *PMEOW;

PCHAR
PrintHex(LPVOID Buffer, int DataLength)
{
    PCHAR result = NULL;
    PBYTE Data = (PBYTE)Buffer;
    CHAR xx[] = "0123456789ABCDEF";
    SIZE_T len = 0;
    if (DataLength != 0)
    {
        len = DataLength <= 20 ? DataLength : 20;
        len <<= 1;
        result = (PCHAR)malloc(len + 1);
        if (result)
        {
            memset(result, 0, len + 1);
            while ((int)--len >= 0)
            {
                result[len] = xx[(Data[len >> 1] >> ((1 - (len & 1)) << 2)) & 0xF];
            }
        }
    }

    return result;
}

PBYTE InitBMP = NULL;
DWORD InitSize = 741 * 641;

void ApplyPatch(PMEOW meoData, DELTA_OUTPUT *lpTarget)
{
    
    PBYTE mem; // ebx
    DELTA_INPUT Patch = {0}; // ST14_12
    DELTA_INPUT InitData = {0}; // ST08_12
    
    if (InitBMP == NULL)
    {
        FILE *hFile = fopen("InitBMP.bmp", "rb");
        if (hFile)
        {
            printf("\nInit BMP data");

            fseek(hFile, 0, SEEK_END);
            DWORD fileSize = ftell(hFile);
            rewind(hFile);
            InitBMP = malloc(fileSize+1);
            if (InitBMP == NULL) 
            {
                fclose(hFile);
                return;
            }
            fread(InitBMP, fileSize, 1, hFile);
            fclose(hFile);
        }
    }
    
    mem = malloc(InitSize);
    if (mem == NULL)
    {
        return;
    }

    printf("\nPrepare Init data from bmp");
    memcpy(mem, InitBMP, InitSize);
    InitData.lpcStart = mem;
    InitData.uSize = InitSize;
    
    printf("\nPrepare Patch data from package");
    Patch.lpcStart = meoData->data;
    Patch.uSize = meoData->PatchSize;
    

    printf("\nApply data patch");
    ApplyDeltaB(0, InitData, Patch, lpTarget);
    
    if (mem)
    {
        free(mem);
    }
    return;
}

void dump_meow_raw_file(PCHAR fileName, PMEOW meowData, size_t pos)
{
    CHAR dumpPath[MAX_PATH] = {0};
    struct stat st = {0};
    DELTA_OUTPUT lpTarget = {0};

    memset(dumpPath, 0, MAX_PATH);
    sprintf(dumpPath, "%s_folder", fileName);
    if (stat(dumpPath, &st) == -1) 
    {
        mkdir(dumpPath, 0700);
    }
    memset(dumpPath, 0, MAX_PATH);
    sprintf(dumpPath, "%s_folder\\%08d_0x%x_0x%x0x%x.raw", fileName, pos, meowData->dwHeader, meowData->dataSize, meowData->PatchSize);
    FILE *meowFile = fopen(dumpPath, "wb");
    // meowData->dwHeader = 0x01444344;
    BYTE meo[] = "meoow";
    if (meowFile)
    {
        // fwrite(&meowData->dwHeader, 4, 1, meowFile);
        // fwrite(&meowData->dataSize, 4, 1, meowFile);
        // fwrite(&meowData->PatchSize, 4, 1, meowFile);
        
        
        //apply path
        ApplyPatch(meowData, &lpTarget);
        if (lpTarget.lpStart != NULL)
        {
            PBYTE outData = malloc(lpTarget.uSize);
            if (outData) 
            {
                memcpy(outData, lpTarget.lpStart, lpTarget.uSize);
                for (int i = 0; i < lpTarget.uSize; i++)
                {
                   outData[i] ^= meo[i%5];
                }
                fwrite(outData, meowData->dataSize, 1, meowFile);
                free(outData);
            }
            memset(&lpTarget, 0, sizeof(DELTA_OUTPUT));
            DeltaFree(lpTarget.lpStart);
        }
        // fwrite(meowData->data, meowData->dataSize, 1, meowFile);
        fclose(meowFile); 
    }
    return;
}

int main(int argc, char* argv[])
{
    size_t pos = 0;
    PMEOW meowData = NULL;
    FILE *hFile = NULL;
    size_t fileSize = 0;
    PCHAR dataBuffer = NULL;
    
    if (argc == 2)
    {

        hFile = fopen(argv[1], "rb");
        if (hFile)
        {
            fseek(hFile, 0, SEEK_END);
            fileSize = ftell(hFile);
            rewind(hFile);
            PBYTE fileBuffer = malloc(fileSize+1);
            if (fileBuffer == NULL) 
            {
                fclose(hFile);
                return -1;
            }
            fread(fileBuffer, fileSize, 1, hFile);

            do 
            {            
                meowData = (PMEOW)(fileBuffer + pos);
                printf("\nData at: 0x%x", pos);
                if (meowData->dwHeader != 0x5730454d)
                {
                    printf("\nInvalid meow header: 0x%x", meowData->dwHeader);
                    break;                    
                }
                printf("\nMEOW header: 0x%x", meowData->dwHeader);
                printf("\nMEOW dataSize: 0x%x", meowData->dataSize);
                printf("\nMEOW PatchSize: 0x%x", meowData->PatchSize);
                dataBuffer = PrintHex(meowData->data, meowData->PatchSize);
                if (dataBuffer) 
                {
                    printf("\nMEOW data: %s", dataBuffer);
                    free(dataBuffer);
                    dataBuffer = NULL;
                }
                dump_meow_raw_file(argv[1], meowData, pos);
                pos += meowData->PatchSize + 12;
            } while (pos < fileSize);
            
            if (fileBuffer)
            {
                free(fileBuffer);
            }
            fclose(hFile);
        }
        printf("\nExtract meow data done");
        if (InitBMP)
        {
            free(InitBMP);
        }
    }
    return 0;
}