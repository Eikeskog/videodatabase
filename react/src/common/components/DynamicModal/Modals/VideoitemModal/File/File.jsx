import React from 'react';
import PropTypes from 'prop-types';

// simple json demo

const File = ({ json }) => (
  <div key="file">
    {/* {Object.keys(json?.[0])?.toString()} */}

    <p key="path">
      Video path:
      <br key="lol" />
      {' '}
      {json?.[0]?.path}
    </p>

    <p key="disk">
      <strong>Disk:</strong>
      <br key="lol2" />
      Name:
      {' '}
      {json?.[0]?.disk?.name}
      <br key="lol3" />
      Id:
      {' '}
      {json?.[0]?.disk?.id}
    </p>

    <p key="project">
      <strong>Project:</strong>
      <br key="lol4" />
      Name:
      {' '}
      {json?.[0]?.project?.name}
      <br key="lol5" />
      Id:
      {' '}
      {json?.[0]?.project?.id}
    </p>

    <p key="dir">
      <strong>Directory:</strong>
      <br key="lol6" />
      Name:
      {' '}
      {json?.[0]?.directory?.name}
      <br key="lol7" />
      Id:
      {' '}
      {json?.[0]?.directory?.id}
      <br key="lol8" />
      Path:
      {' '}
      {json?.[0]?.directory?.path}
      <br key="lol9" />
      Rolltype:
      {' '}
      {json?.[0]?.directory?.rolltype}
      <br key="lol10" />
      Directory items:
      {' '}
      <br key="lol11" />
      {json?.[0]?.directory?.videoitems?.map((videoitem) => (
        <React.Fragment key={videoitem.id}>
          {videoitem.id}
          <br />
        </React.Fragment>
      ))}
    </p>

  </div>
);

export default File;

File.propTypes = {
  json: PropTypes.arrayOf(
    PropTypes.shape({
      path: PropTypes.string,
      disk: PropTypes.shape({
        id: PropTypes.string,
        name: PropTypes.string,
      }),
      project: PropTypes.shape({
        id: PropTypes.string,
        name: PropTypes.string,
      }),
      directory: PropTypes.shape({
        id: PropTypes.number,
        name: PropTypes.string,
        path: PropTypes.string,
        rolltype: PropTypes.string,
        videoitems: PropTypes.arrayOf(
          PropTypes.shape({
            id: PropTypes.string,
            lat: PropTypes.number,
            lng: PropTypes.number,
            thumbnail_count: PropTypes.number,
          }),
        ),
      }),
    }),
  ),
};

File.defaultProps = {
  json: null,
};
