from retrieval_classes import Solicitud, DataFetcher

def main():
    # Coordinates for David, Chiriquí, Panama
    coords = (-82.43, 8.43)

    # Request multiple variables
    solicitud = Solicitud(coords).hacer_solicitud(
        variables=['radiacion solar', 'temperatura', 'precipitacion', 'velocidad viento']
    )

    # Fetch data
    fetcher = DataFetcher(solicitud)
    df = fetcher.to_dataframe()

    # Display results
    print("Retrieved Climate Data:")
    print(df)

if __name__ == "__main__":
    main()
