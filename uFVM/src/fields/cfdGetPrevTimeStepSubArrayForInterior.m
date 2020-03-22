function phi = cfdGetPrevTimeStepSubArrayForInterior(theFieldName, iComponent)
%--------------------------------------------------------------------------
%
%  Written by the CFD Group @ AUB, Fall 2018
%  Contact us at: cfd@aub.edu.lb
%==========================================================================
% Routine Description:
%   This function returns a subarray at interior elements
%--------------------------------------------------------------------------

if nargin==1
    iComponent = 1;
end

global Region;

if strcmp(Region.fluid.(theFieldName).type, 'cfdSurfaceScalarField')
    phi = Region.fluid.(theFieldName).prevTimeStep.phi(1:Region.mesh.numberOfInteriorFaces);    
else
    phi = Region.fluid.(theFieldName).prevTimeStep.phi(1:Region.mesh.numberOfElements, iComponent);
end
