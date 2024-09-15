#include <iostream>
using namespace std;

void bubble_sort(int arr[], int n)
{

    for (int i = n - 1; i > 0; i--)
    {
        for (int j = 0; j < n - 1; j++)
        {
            if (arr[j] > arr[j + 1])
            {
                int temp = arr[j + 1];
                arr[j + 1] = arr[j];
                arr[j] = temp;
            }
        }
    }
}

void print_arr(int arr[], int n)
{
    for (int i = 0; i < n; i++)
    {
        cout << arr[i] << " ";
    }
    cout << endl;
}

int main()
{
    int arr[] = {1, 5332, 4, 13412, 5233213, 412325, 412312, 233123, 23123, 2423};

    int size = sizeof(arr) / sizeof(arr[0]);

    bubble_sort(arr, size);

    cout << "Sorted array: ";
    print_arr(arr, size);
    return 0;
}
