import React from "react";
// @ts-ignore
import {Bar, Line} from 'react-chartjs-2';
import Header from "../components/Header.tsx";

function DangerRatings(data:any) {
    console.log(data)
    let rows: any[] = []
    data.data.forEach((day:any) => {
        rows.push(
            <tr>
                <td>{day.date.display}</td>
                <td>{day.ratings.alp.display}</td>
                <td>{day.ratings.alp.rating.display}</td>
            </tr>
        )
        rows.push(
            <tr>
                <td>{day.date.display}</td>
                <td>{day.ratings.tln.display}</td>
                <td>{day.ratings.tln.rating.display}</td>
            </tr>
        )
        rows.push(
            <tr>
                <td>{day.date.display}</td>
                <td>{day.ratings.btl.display}</td>
                <td>{day.ratings.btl.rating.display}</td>
            </tr>
        )
    })
    return (
        <table>
            <tr>
                <th>Date</th>
                <th>Elevation</th>
                <th>Risk Level</th>
            </tr>
            {rows}
        </table>
    )
}
function AvalancheForecast() {
    let [forecast, setForecast]:[any, any] = React.useState(null);

    React.useEffect(() => {
        let url = "/api/avalanche_forecast";
        if ("localhost" === window.location.hostname) {
            url = "http://localhost:5040/api/avalanche_forecast";
        }
        fetch(url).then((response) => {
            response.json().then((data) => {
                setForecast(data);
            });
        });
    }, []);

    if (!forecast) {
        return <div>Loading...</div>;
    }

    let problems: any[] = []
    forecast.report.problems.forEach((problem:any) => {
        let aspects: any[] = []
        problem.data.aspects.forEach((aspect:any) => {
            aspects.push(
                <div>
                    {aspect.display}
                 </div>
            )
        })
        problems.push(
            <div>
                <div> {problem.type.display}</div>
                <div dangerouslySetInnerHTML={{ __html: problem.comment}} />
                <div> {aspects} </div>
            </div>
        )
    })

    let summaries: any[] = []
    forecast.report.summaries.forEach((summary:any) => {
        summaries.push(
            <div>
                <h3>{summary.type.display}</h3>
                <div dangerouslySetInnerHTML={{ __html: summary.content}} />
                </div>
        )
    })

    let advice: any[] = []
    forecast.report.terrainAndTravelAdvice.forEach((a:any) => {
        advice.push(<li>{a}</li>)
    })

    return (
        <div>
            <Header/>
            <h1>Avalanche Forecast</h1>
            <table>
                <tr><td>Issued:</td><td>{forecast.report.dateIssued}</td></tr>
                <tr><td>Highlights:</td><td><div dangerouslySetInnerHTML={{ __html:forecast.report.highlights}}/>
                </td></tr>
            </table>
            <h2>Danger Ratings</h2>
            <DangerRatings data={forecast.report.dangerRatings}/>
            <h2>Problems</h2>
            {problems}
            <h2>Summaries</h2>
            {summaries}
            <h2>Terrain And Travel Advice</h2>
            <ul>{advice}</ul>
        </div>
    );
}

export default AvalancheForecast;

