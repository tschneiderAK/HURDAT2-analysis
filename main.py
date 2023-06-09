import logging
from datetime import datetime
import services
import repositories
import entities
import constants


def main():

    # Set up logging.
    logging.basicConfig(filename='app.log', filemode='w', level=logging.INFO)
    logging.info('Analysis Started at' + str(datetime.now()))
    
    # Initialize the area service.
    area_service = services.AreaService(repositories.AreaJSONRepository,
                                        constants.FLORIDA_GEOJSON)

    # Initilize the storm data service.
    # TODO: Add config details for which repository to call. Default to StormTextRepository.
    data_service = services.StormDataService(repo=repositories.StormTextRepository,
                                             source_path=constants.HURDAT_DATA,
                                             area=area_service)
    
    # Initialize report service.
    report_service = services.ReportService(repositories.JSONReportRepository)

    # Extract a list of storm Tracks.
    events = data_service.record_landfall_events()

    # Generate and save the report.
    report_service.generate(events)
    report_save_status = report_service.save(constants.REPORT)
    
    # Check save return code and log errors.
    if report_save_status != 200:
        logging.warning('Error: Report not saved. Check file directory configurations and try again.')
        
if __name__ == "__main__":
    main()