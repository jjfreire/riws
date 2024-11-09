import React, { useState } from "react";

import ElasticsearchAPIConnector from "@elastic/search-ui-elasticsearch-connector";

import {
  ErrorBoundary,
  Facet,
  SearchProvider,
  SearchBox,
  Results,
  PagingInfo,
  ResultsPerPage,
  Paging,
  Sorting,
  WithSearch
} from "@elastic/react-search-ui";
import { Layout } from "@elastic/react-search-ui-views";
import "@elastic/react-search-ui-views/lib/styles/styles.css";

import {
  buildAutocompleteQueryConfig,
  buildFacetConfigFromConfig,
  buildSearchOptionsFromConfig,
  buildSortOptionsFromConfig,
  getConfig,
  getFacetFields
} from "./config/config-helper";

const { hostIdentifier, searchKey, endpointBase, engineName } = getConfig();
const connector = new ElasticsearchAPIConnector({
  host: "http://localhost:9200",
  index: "jobs"
});
const config = {
    searchQuery: {

      //Campos por los que se puede hacer la búsqueda
      search_fields: {
        title: {
          weight: 3
        },
        description: {
          weight: 2
        },
        location: {
          weight: 1
        },
        company: {
          weight: 1
        },
        workday: {
          weight: 1
        },
        modality: {
          weight: 2
        },
        duration: {
          weight: 1
        }
      },

      //Campos que se muestran de los resultados de la búsqueda
      result_fields: {
        title: {
          snippet: {}
        },
        description: {
          snippet: {}
        },
        min_salary: {
          raw: {}
        },
        max_salary: {
          raw: {}
        },
        location: {
          raw: {}
        },
        company: {
          raw: {}
        },
        workday: {
          raw: {}
        },
        modality: {
          raw: {}
        },
        duration: {
          raw: {}
        },
        link: {
          raw: {}
        },
        image: {
          raw: {}
        }

      },

      //Filtros que quieres que actuen con un OR
      disjunctiveFacets: ["modality.keyword", "workday.keyword", "location.keyword", "company.keyword", "duration.keyword"],

      //Configuración de los filtros
      facets: {
        "modality.keyword": { type: "value" },
        "workday.keyword": { type: "value" },
        "location.keyword": { type: "value" },
        "company.keyword": { type: "value" },
        "duration.keyword": { type: "value" },

        min_salary: {
          type: "range",
          ranges: [
            { from: 0, to: 20000, name: "0-20k" },
            { from: 20000, to: 40000, name: "20k-40k" },
            { from: 40000, to: 60000, name: "40k-60k" },
            { from: 60000, to: 80000, name: "60k-80k" },
            { from: 80000, name: "80k+" }
            ]
        }

      }
    },
    
    autocompleteQuery: {
      results: {
        resultsPerPage: 5,
        search_fields: {
          "title": {
            weight: 3
          }
        },
        result_fields: {
          title: {
            snippet: {
              size: 100,
              fallback: true
            }
          },
          link: {
            raw: {}
          }
        }
      },

      //Para usar suggestions tendríamos que tener un campo de tipo completion en el índice
    
    },
    apiConnector: connector,
    alwaysSearchOnInitialLoad: true
  
};

const CustomResultView = ({ result }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  const toggleExpanded = () => {
    setIsExpanded(!isExpanded);
  };

  const descriptionText = result.description.raw || "";
  const shortenedDescription = descriptionText.slice(0, 150);

  return (
    <li className="sui-result">
      <div className="sui-result__header">
        <a
          className="sui-result__title sui-result__title-link"
          href={result.link.raw}
          target="_blank"
          rel="noopener noreferrer"
        >
          {result.title.raw}
        </a>
      </div>
      <div className="sui-result__body">
        <div className="sui-result__image">
          {result.image && <img src={result.image.raw} alt={result.title.raw} />}
        </div>
        <ul className="sui-result__details">
          <li>
            <span className="sui-result__title-link">Company: </span>{" "}
            <span className="sui-result__value">{result.company.raw}</span>
          </li>
          <li>
              <span className="sui-result__title-link">Description: </span>{" "}
              <span className="sui-result__value">
                {isExpanded ? descriptionText : `${shortenedDescription}... `}
                <button onClick={toggleExpanded} className="toggle-button">
                  {isExpanded ? "Ver menos" : "Ver más"}
                </button>
              </span>
            </li>
          <li>
            <span className="sui-result__title-link">Min_salary: </span>{" "}
            <span className="sui-result__value">{result.min_salary && result.min_salary.raw ? result.min_salary.raw + "€": "N/A"}</span>
          </li>
          <li>
            <span className="sui-result__title-link">Max_salary: </span>{" "}
            <span className="sui-result__value">{result.max_salary && result.max_salary.raw ? result.max_salary.raw + "€" : "N/A"}</span>
          </li>
          <li>
            <span className="sui-result__title-link">Duration: </span>{" "}
            <span className="sui-result__value">{result.duration.raw}</span>
          </li>
          <li>
            <span className="sui-result__title-link">Workday: </span>{" "}
            <span className="sui-result__value">{result.workday.raw}</span>
          </li>
          <li>
            <span className="sui-result__title-link">Location: </span>{" "}
            <span className="sui-result__value">{result.location.raw}</span>
          </li>
          <li>
            <span className="sui-result__title-link">Modality: </span>{" "}
            <span className="sui-result__value">{result.modality.raw}</span>
          </li>
        </ul>
      </div>
    </li>
  );
}

export default function App() {
  return (
    <SearchProvider config={config}>
      <WithSearch mapContextToProps={({ wasSearched }) => ({ wasSearched })}>
        {({ wasSearched }) => {
          return (
            <div className="App">
              <ErrorBoundary>
                <Layout
                  header={
                    <SearchBox
                      autocompleteMinimumCharacters={3}
                      autocompleteResults={{
                        linkTarget: "_blank",
                        sectionTitle: "Results",
                        titleField: "title",
                        urlField: "link",
                        shouldTrackClickThrough: true
                      }}
                      autocompleteSuggestions={true}
                      debounceLength={0}
                    />
                  }
                  sideContent={
                    <div>
                      <Facet key={"6"} field={"min_salary"} label={"Salary"} />
                      <Facet key={"1"} field={"modality.keyword"} label={"Modality"} />
                      <Facet key={"2"} field={"workday.keyword"} label={"Workday"} />
                      <Facet key={"3"} field={"location.keyword"} label={"Location"} />
                      <Facet key={"4"} field={"company.keyword"} label={"Company"} />
                      <Facet key={"5"} field={"duration.keyword"} label={"Duration"} />
                    </div>
                  }
                  bodyContent={
                    <Results
                      titleField="title"
                      urlField="link"
                      thumbnailField="image"
                      shouldTrackClickThrough={true}
                      resultView={CustomResultView}
                    />
                  }
                  bodyHeader={
                    <React.Fragment>
                      {wasSearched && <PagingInfo />}
                      {wasSearched && <ResultsPerPage />}
                    </React.Fragment>
                  }
                  bodyFooter={<Paging />}
                />
              </ErrorBoundary>
            </div>
          );
        }}
      </WithSearch>
    </SearchProvider>
  );
}
